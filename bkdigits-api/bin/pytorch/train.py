#!/usr/bin/env python3

import os
import requests
import torch
import torch.distributed
import torch.nn as nn

from argparse import ArgumentParser


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--nodes', required=True)
    parser.add_argument('--shuffle', action='store_true')
    parser.add_argument('--dataset-path', required=True)
    parser.add_argument('--val-dataset-path', required=True)
    parser.add_argument('--job-path', required=True)
    parser.add_argument('--epochs', type=int, required=True)
    parser.add_argument('--node-type', required=True)

    return parser.parse_args()


NODE_TO_DIST_CLS = {
    'cpu': nn.parallel.DistributedDataParallelCPU,
    'gpu': nn.parallel.DistributedDataParallel
}


if __name__ == "__main__":
    args = parse_arguments()

    nodes = args.nodes.split(',')
    
    log_dir = os.path.join(args.job_path, 'logs')
    snapshot_dir = os.path.join(args.job_path, 'snapshots')
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(snapshot_dir, exist_ok=True)
