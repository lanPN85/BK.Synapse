#!/usr/bin/env bash

VERSION=0.1.0

nvidia-docker build -t bksynapse/base-gpu:${VERSION}\
    -t bksynapse/base-gpu:latest -f Dockerfile-GPU .
