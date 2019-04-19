#!/usr/bin/env bash

VERSION=0.1.0

docker build -t bksynapse/base:${VERSION}\
    -t bksynapse/base:latest --no-cache .
