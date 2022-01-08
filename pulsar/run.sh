#!/usr/bin/env bash

_PULSAR_DATA="$PWD/puslar/data"

[ ! -d $_PULSAR_DATA ] && mkdir $_PULSAR_DATA

docker run -it \
    -p 6650:6650 \
    -p 8080:8080 \
    -v $_PULSAR_DATA:/pulsar/data \
    apachepulsar/pulsar:latest \
    bin/pulsar standalone
