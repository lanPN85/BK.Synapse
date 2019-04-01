#!/usr/bin/env bash
SERVICE=${1-"app-main"}

docker-compose exec ${SERVICE} bash
