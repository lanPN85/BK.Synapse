#!/usr/bin/env python

import sys
sys.path.extend(['.'])
import os
import signal
import logging
import logzero
import torch
import shutil
import traceback
import torch.distributed
import torch.nn as nn
import torch.optim as optim
import torch.cuda
import horovod.torch as hvd
import tensorboardX

from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler
from argparse import ArgumentParser
from logzero import logger
from collections import defaultdict

from bksyn.datasets import Dataset as BkDigitsDataset
from bksyn.jobs import TrainingJob, TrainingJobStatus, TrainingJobMetric
from bksyn.loaders import DataLoader as BkDigitsDataLoader
from bksyn.models import Model
from bksyn.metrics import UpdatingMetric


hvd.init()

def root_node_only(fn):
    def decorate(*args, **kwargs):
        if hvd.rank() == 0:
            return fn(*args, **kwargs)
    return decorate


def handle_exit(sig, frame):
    raise(SystemExit)

signal.signal(signal.SIGTERM, handle_exit)


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


@root_node_only
def save_tensorboard_graph(log_writer, model, inp):
    log_writer.add_graph(model, (inp,))


@root_node_only
def save_tensorboard_metrics(log_writer, metrics, epoch, prefix=''):
    for mt in metrics:
        log_writer.add_scalar('%s%s' % (prefix, mt.name),
            mt.value, epoch)

    
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
    for mt in kwargs['metrics']:
        logger.info('\t%s: %.5f' % (mt.name, mt.value))

@root_node_only
def save_snapshot(model, path):
    torch.save(model.state_dict(), path)


OPTIMIZER_MAP = {
    'sgd': optim.SGD, 'adam': optim.Adam, 
    'adadelta': optim.Adadelta, 'rmsprop': optim.RMSprop
}


def main(job):
    logzero.logfile(os.path.join(job.log_path, 'train.node-%d.log' % hvd.rank()),mode='w')
    if hvd.rank() == 0:
        if os.path.exists(job.history_path):
            os.remove(job.history_path)
    log_update_status(job, state='SETUP')

    # Setup objects
    model = Model.load(job.config.model)
    _loader = BkDigitsDataLoader.load(job.config.dataLoader)
    _val_loader = BkDigitsDataLoader.load(job.config.valDataLoader)
    _dataset = BkDigitsDataset(job.config.dataset)
    _val_dataset = BkDigitsDataset(job.config.valDataset)
    assert job.config.backend == 'pytorch'
    assert model.backend == 'pytorch'

    optim_cls = OPTIMIZER_MAP[job.config.optimizer]

    try:
        # Import data loader
        train_dataset = _loader.get_dataset(_dataset.path)
        val_dataset = _val_loader.get_dataset(_val_dataset.path, val=True)
    except (NameError, AttributeError):
        log_update_status(job, state='ERROR', message="Invalid data loader")
        exit(-1)
    
    try:
        # Import model
        torch_model = model.load_model()
    except AttributeError:
        log_update_status(job, state='ERROR', 
            message="Input model must implement loss(output, target)")
        exit(-1)

    use_cuda = job.config.nodeType == 'gpu'
    kwargs = {}
    if use_cuda:
        torch.cuda.set_device(hvd.local_rank())
        kwargs = {'num_workers': 1, 'pin_memory': True}
        torch_model.cuda()
    else:
        torch_model.cpu()
    
    # Setup data samplers
    train_sampler = DistributedSampler(train_dataset, num_replicas=hvd.size(), rank=hvd.rank())
    train_loader = DataLoader(train_dataset,
        batch_size=job.config.batchSize,
        sampler=train_sampler, 
        collate_fn=train_dataset.collate, **kwargs)
    
    val_sampler = DistributedSampler(val_dataset, num_replicas=hvd.size(), rank=hvd.rank())
    val_loader = DataLoader(val_dataset,    
        batch_size=job.config.batchSize,
        sampler=val_sampler, collate_fn=val_dataset.collate, **kwargs)

    # Setup optimizers
    hvd.broadcast_parameters(torch_model.state_dict(), root_rank=0)
    optimizer = optim_cls(torch_model.parameters(),
        lr=job.config.learningRate * hvd.size())
    compression = hvd.Compression.none
    optimizer = hvd.DistributedOptimizer(optimizer,
        named_parameters=torch_model.named_parameters(),
        compression=compression)

    # Setup tensorboard
    tb_path = os.path.join(job.output_path, 'tensorboard')
    if hvd.rank() == 0:
        if os.path.exists(tb_path):
            shutil.rmtree(tb_path)
    log_writer = tensorboardX.SummaryWriter(tb_path) if hvd.rank() == 0 else None
    # Visualize graph with first batch
    first_batch, _ = next(iter(val_loader))
    if use_cuda:
        first_batch = first_batch.cuda()
    try:
        save_tensorboard_graph(log_writer, torch_model, first_batch)
    except RuntimeError:
        pass
    del first_batch

    # Start training
    log_update_status(job, state='TRAINING', message='Starting training...')
    avg_metrics = []
    for ep in range(job.config.epochs):
        # Check for lock
        if os.path.exists(job.stop_lock_path):
            log_update_status(job, state='INTERRUPT', metrics=avg_metrics)
            exit(-1)
        
        # Train phase
        torch_model.train()
        train_sampler.set_epoch(ep)
        metrics = defaultdict(lambda: UpdatingMetric())
        for batch_idx, (data, target) in enumerate(train_loader):
            if use_cuda:
                if isinstance(data, list) or isinstance(data, tuple):
                    data = list(map(lambda x: x.cuda(), data))
                else:
                    data = data.cuda()
                
                if isinstance(target, list) or isinstance(target, tuple):
                    target = list(map(lambda x: x.cuda(), target))
                else:
                    target = target.cuda()
        
            optimizer.zero_grad()
            output = torch_model(data)
            loss = torch_model.loss(output, target)
            loss.backward()
            optimizer.step()
            metrics['loss'].update(loss.item())
            
            try:
                # Get metrics if metrics() is implemented
                _user_metrics = torch_model.metrics(output, target)
                for k, v in _user_metrics.items():
                    metrics[k].update(v)
            except AttributeError:
                pass
            
            # Convert Metric to value
            m_list = []
            for k, v in metrics.items():
                m_list.append(TrainingJobMetric(name=k, value=v.avg))
            m_list.extend(avg_metrics)

            log_update_status(job, state='TRAINING',
                iter=batch_idx+1, totalIter=len(train_loader), epoch=ep+1, metrics=m_list)
            # Check for lock
            if os.path.exists(job.stop_lock_path):
                log_update_status(job, state='INTERRUPT')
                exit(-1)
        
        m_list = []
        for k, v in metrics.items():
            m_list.append(TrainingJobMetric(name=k, value=v.avg))
        m_list.extend(avg_metrics)
        save_tensorboard_metrics(log_writer, m_list, 
            ep+1, prefix='train/')

        # Eval phase
        torch_model.eval()
        val_metrics = defaultdict(lambda: 0.)
        log_update_status(job, state='EVALUATING', epoch=ep+1, 
            metrics=avg_metrics)
        for batch_idx, (data, target) in enumerate(val_loader):
            if use_cuda:
                if isinstance(data, list) or isinstance(data, tuple):
                    data = list(map(lambda x: x.cuda(), data))
                else:
                    data = data.cuda()
                
                if isinstance(target, list) or isinstance(target, tuple):
                    target = list(map(lambda x: x.cuda(), target))
                else:
                    target = target.cuda()
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
            # Check for lock
            if os.path.exists(job.stop_lock_path):
                log_update_status(job, state='INTERRUPT', metrics=avg_metrics)
                exit(-1)
        
        # Calculate average for all metrics
        avg_metrics = []
        kv_list = sorted(val_metrics.items(), key=lambda x: x[0])
        for k, v in kv_list:
            avg_k = 'val_%s' % k
            avg_v = v / len(val_loader)
            avg_v = metric_average(avg_v, avg_k)
            avg_metrics.append(TrainingJobMetric(name=avg_k, value=avg_v))

            # Check for lock
            if os.path.exists(job.stop_lock_path):
                log_update_status(job, state='INTERRUPT', metrics=avg_metrics)
                exit(-1)
        log_update_status(job, state='EVALUATED', epoch=ep+1,
            iter=len(val_loader), metrics=avg_metrics, 
            totalIter=len(val_loader))
        save_tensorboard_metrics(log_writer, avg_metrics, ep+1, prefix='val/')

        # Save snapshot
        if ep % job.config.snapshotInterval == 0 and hvd.rank() == 0:
            snap_path = os.path.join(job.snapshot_path, 
                job.get_snapshot_name(ep + 1))
            save_snapshot(torch_model, snap_path)
            log_update_status(job, state='SAVING', 
                message='Saved model snapshot', 
                metrics=avg_metrics, epoch=ep+1)
    
    if log_writer:
        log_writer.close()
    log_update_status(job, state='FINISHED', metrics=avg_metrics)


if __name__ == "__main__":
    args = parse_arguments()
    job = TrainingJob.load(args.job_id)
    try:
        main(job)
    except SystemExit:
        log_update_status(job, state='INTERRUPT')
    except:
        log_update_status(job, state='ERROR', message=traceback.format_exc())
