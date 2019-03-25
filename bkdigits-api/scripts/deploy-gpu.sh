#!/usr/bin/env bash

set -e

docker-compose -f docker-compose.yml -f docker-compose.gpu.yml down
docker-compose -f docker-compose.yml -f docker-compose.gpu.yml build
docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up
