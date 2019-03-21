#!/usr/bin/env python3

import sys
sys.path.extend(['.'])
import os
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

from apis import utils
from bkdigits.datasets import Dataset as BkDigitsDataset
from bkdigits.jobs import TrainingJob, TrainingJobStatus
from bkdigits.loaders import DataLoader as BkDigitsDataLoader
from bkdigits.models import Model


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
    tensor = torch.Tensor(val)
    avg_tensor = hvd.allreduce(tensor, name=name)
    return avg_tensor.item()


def update_job_status(job, **kwargs):
    status = TrainingJobStatus(**kwargs)
    job.update_status(status)


NODE_TO_DIST_CLS = {
    'cpu': nn.parallel.DistributedDataParallelCPU,
    'gpu': nn.parallel.DistributedDataParallel
}

OPTIMIZER_MAP = {
    'sgd': optim.SGD, 'adam': optim.Adam, 
    'adadelta': optim.Adadelta, 'rmsprop': optim.RMSprop
}


if __name__ == "__main__":
    args = parse_arguments()

    job = TrainingJob.load(args.job_id)
    model = Model.load(job.config.model)
    _loader = BkDigitsDataLoader.load(job.config.dataLoader)
    _val_loader = BkDigitsDataLoader.load(job.config.valDataLoader)
    _dataset = BkDigitsDataset(job.config.dataset)
    _val_dataset = BkDigitsDataset(job.config.valData)
    assert job.config.backend == 'pytorch'
    assert model.backend == 'pytorch'

    logzero.logfile(os.path.join(job.log_path, 'train.node-%d.log' % hvd.rank()))
    dist_cls = NODE_TO_DIST_CLS[job.config.nodeType]
    optim_cls = OPTIMIZER_MAP[job.config.optimizer]

    try:    
        try:
            # Import data loader
            train_dataset = _loader.get_dataset(_dataset.path)
            val_dataset = _val_loader.get_dataset(_val_dataset.path)
        except NameError, AttributeError:
            update_job_status(state='ERROR', message="Invalid data loader")
            exit(-1)
        
        try:
            torch_model = model.load_model()
        except AttributeError:
            update_job_status(running=False, 
                error="Input model must implement loss()")
            exit(-1)

        use_cuda = job.config.nodeType == 'gpu'
        hvd.init()
        kwargs = {}
        if use_cuda:
            torch.cuda.set_device(hvd.local_rank())
            kwargs = {'num_workers': 1, 'pin_memory': True}
            torch_model.cuda()
        else:
            torch_model.cpu()
        
        train_sampler = DistributedSampler(train_dataset, num_replicas=hvd.size(), rank=hvd.rank())
        train_loader = DataLoader(train_dataset, 
            batch_size=job.config.batchSize, shuffle=job.config.shuffle,
            sampler=train_sampler, collate_fn=train_dataset.collate, **kwargs)
        
        val_sampler = DistributedSampler(val_dataset, num_replicas=hvd.size(), rank=hvd.rank())
        val_loader = DataLoader(val_dataset, 
            batch_size=job.config.batchSize, shuffle=job.config.shuffle,
            sampler=val_sampler, collate_fn=val_dataset.collate, **kwargs)

        hvd.broadcast_parameters(torch_model.state_dict(), root_rank=0)
        optimizer = optim_cls(torch_model.parameters(),
            lr=job.config.learningRate * hvd.size())
        compression = hvd.Compression.none
        optimizer = hvd.DistributedOptimizer(optimizer,
            named_parameters=torch_model.named_parameters(),
            compression=compression)
    except Exception as e:
        update_job_status(state='ERROR', message=traceback.format_exc())
        exit(-1)

    # Start training
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

        # Eval phase
        torch_model.eval()
        val_loss = 0.
        for batch_idx, (data, target) in enumerate(val_loader):
            if use_cuda:
                data, target = data.cuda(), target.cuda()
            output = torch_model(data)
            loss = torch_model.loss(output, target).item
            val_loss += loss
        
        val_loss /= len(test_sampler)
        val_loss = metric_average(val_loss, 'avg_loss')
