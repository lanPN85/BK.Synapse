#!/usr/bin/env bash

docker run --rm -it\
    -e BKSYN_DATA_ROOT=/app/tests/data\ 
    -v $PWD:/app bksynapse/api:0.1.0\
    /app/bin/pytorch/train.py --job-id test-torch
