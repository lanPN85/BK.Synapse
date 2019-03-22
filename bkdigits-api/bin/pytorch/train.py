#!/usr/bin/env python3

import sys
sys.path.extend(['.'])
import os
import logging
import requests
import logzero
import torch
import traceback
import torch.distributed
import torch.nn as nn
import torch.optim as optim
import torch.cuda
import horovod.torch as hvd

from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler
from argparse import ArgumentParser
from logzero import logger
from collections import defaultdict

from apis import utils
from bkdigits.datasets import Dataset as BkDigitsDataset
from bkdigits.jobs import TrainingJob, TrainingJobStatus
from bkdigits.loaders import DataLoader as BkDigitsDataLoader
from bkdigits.models import Model


hvd.init()

def root_node_only(fn):
    def decorate(*args, **kwargs):
        if hvd.rank() == 0:
            return fn(*args, **kwargs)
    return decorate


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--job-id', required=True)
    return parser.parse_args()


def metric_average(val, name):
    tensor = torch.Tensor([val])
    avg_tensor = hvd.allreduce(tensor, name=name)
    return avg_tensor.item()


@root_node_only
def update_job_status(job, **kwargs):
    status = TrainingJobStatus(**kwargs)
    job.update_status(status)

    
def log_update_status(job, **kwargs):
    update_job_status(job, **kwargs)

    kwargs['iter'] = kwargs.get('iter', 0)
    kwargs['totalIter'] = kwargs.get('totalIter', 0)
    kwargs['epoch'] = kwargs.get('epoch', 0)
    kwargs['totalEpoch'] = job.config.epochs
    kwargs['message'] = kwargs.get('message', '')
    kwargs['metrics'] = kwargs.get('metrics', {})

    LOG_LEVEL = defaultdict(lambda: logging.DEBUG, {
        'TRAINING': logging.INFO,
        'EVALUATING': logging.INFO,
        'ERROR': logging.ERROR,
        'INTERRUPT': logging.WARN
    })
    logger.log(LOG_LEVEL[kwargs['state']], '[{state} I{iter}/{totalIter} E{epoch}/{totalEpoch}] {message}'.format(**kwargs))
    for k, v in kwargs['metrics'].items():
        logger.info('\t%s: %.5f' % (k, v))

@root_node_only
def save_snapshot(model, path):
    torch.save(model.state_dict(), path)

NODE_TO_DIST_CLS = {
    'cpu': nn.parallel.DistributedDataParallelCPU,
    'gpu': nn.parallel.DistributedDataParallel
}

OPTIMIZER_MAP = {
    'sgd': optim.SGD, 'adam': optim.Adam, 
    'adadelta': optim.Adadelta, 'rmsprop': optim.RMSprop
}


def main(job):
    if os.path.exists(job.history_path):
        os.remove(job.history_path)
    log_update_status(job, state='SETUP')
    model = Model.load(job.config.model)
    _loader = BkDigitsDataLoader.load(job.config.dataLoader)
    _val_loader = BkDigitsDataLoader.load(job.config.valDataLoader)
    _dataset = BkDigitsDataset(job.config.dataset)
    _val_dataset = BkDigitsDataset(job.config.valDataset)
    assert job.config.backend == 'pytorch'
    assert model.backend == 'pytorch'

    logzero.logfile(os.path.join(job.log_path, 'train.node-%d.log' % hvd.rank()),mode='w')
    dist_cls = NODE_TO_DIST_CLS[job.config.nodeType]
    optim_cls = OPTIMIZER_MAP[job.config.optimizer]

    try:
        # Import data loader
        train_dataset = _loader.get_dataset(_dataset.path)
        val_dataset = _val_loader.get_dataset(_val_dataset.path)
    except (NameError, AttributeError):
        log_update_status(state='ERROR', message="Invalid data loader")
        exit(-1)
    
    try:
        torch_model = model.load_model()
    except AttributeError:
        log_update_status(running=False, 
            error="Input model must implement loss(output, target)")
        exit(-1)

    use_cuda = job.config.nodeType == 'gpu'
    kwargs = {}
    if use_cuda:
        torch.cuda.set_device(hvd.local_rank())
        kwargs = {'num_workers': 1, 'pin_memory': True}
        torch_model.cuda()
    else:
        torch_model.cpu()
    
    train_sampler = DistributedSampler(train_dataset, num_replicas=hvd.size(), rank=hvd.rank())
    train_loader = DataLoader(train_dataset,
        batch_size=job.config.batchSize,
        sampler=train_sampler, 
        collate_fn=train_dataset.collate, **kwargs)
    
    val_sampler = DistributedSampler(val_dataset, num_replicas=hvd.size(), rank=hvd.rank())
    val_loader = DataLoader(val_dataset,    
        batch_size=job.config.batchSize,
        sampler=val_sampler, collate_fn=val_dataset.collate, **kwargs)

    hvd.broadcast_parameters(torch_model.state_dict(), root_rank=0)
    optimizer = optim_cls(torch_model.parameters(),
        lr=job.config.learningRate * hvd.size())
    compression = hvd.Compression.none
    optimizer = hvd.DistributedOptimizer(optimizer,
        named_parameters=torch_model.named_parameters(),
        compression=compression)

    # Start training
    log_update_status(job, state='TRAINING', message='Starting training...')
    for ep in range(job.config.epochs):
        # Train phase
        torch_model.train()
        train_sampler.set_epoch(ep)
        for batch_idx, (data, target) in enumerate(train_loader):
            if use_cuda:
                data, target = data.cuda(), target.cuda()
        
            optimizer.zero_grad()
            output = torch_model(data)
            loss = torch_model.loss(output, target)
            loss.backward()
            optimizer.step()
            metrics = {'loss': loss.item()}
            try:
                # Get metrics if metrics() is implemented
                metrics.update(torch_model.metrics(output, target))
            except AttributeError:
                pass
            log_update_status(job, state='TRAINING',
                iter=batch_idx+1, totalIter=len(train_loader), epoch=ep+1, metrics=metrics)

        # Eval phase
        torch_model.eval()
        val_metrics = defaultdict(lambda: 0.)
        log_update_status(job, state='EVALUATING', epoch=ep+1)
        for batch_idx, (data, target) in enumerate(val_loader):
            if use_cuda:
                data, target = data.cuda(), target.cuda()
            output = torch_model(data)
            metrics
            loss = torch_model.loss(output, target).item()
            val_metrics['loss'] += loss
            try:
                # Get metrics if metrics() is implemented
                _user_metrics = torch_model.metrics(output, target)
                for k, v in _user_metrics.items():
                    val_metrics[k] += v
            except:
                pass

            log_update_status(job, state='EVALUATING', epoch=ep+1, iter=batch_idx+1,totalIter=len(val_loader))
        
        # Calculate average for all metrics
        avg_metrics = {}
        for k, v in val_metrics.items():
            avg_k = 'avg_%s' % k
            avg_v = v / len(val_loader)
            avg_v = metric_average(avg_v, avg_k)
            avg_metrics[avg_k] = avg_v
        log_update_status(job, state='EVALUATED', epoch=ep+1,
            iter=len(val_loader), metrics=avg_metrics, 
            totalIter=len(val_loader))

        # Save snapshot
        if ep % job.config.snapshotInterval == 0:
            snap_path = os.path.join(job.snapshot_path, 
                'epoch-%d.pth' % (ep+1))
            save_snapshot(torch_model, snap_path)
            log_update_status(job, state='SAVING', 
                message='Saved model snapshot')
        
    log_update_status(job, state='FINISHED')


if __name__ == "__main__":
    args = parse_arguments()
    job = TrainingJob.load(args.job_id)
    try:
        main(job)
    except KeyboardInterrupt:
        log_update_status(job, state='INTERRUPT', message="Training interrupted")
    except:
        log_update_status(job, state='ERROR', message=traceback.format_exc())
