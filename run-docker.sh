#!/usr/bin/env bash

docker build -t discussions .
docker run --name discussions-container -p 8001:8001 discussions
