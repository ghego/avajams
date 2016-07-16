#!/bin/bash

docker run --rm -v "$PWD":/worker -w /worker iron/python:2-dev pip install -t packages -r requirements.txt
docker run --rm -e "PAYLOAD_FILE=hello.payload.json" -e "YOUR_ENV_VAR=ANYTHING" -v "$PWD":/worker -w /worker iron/python:2 python hello.py
docker build -t mistobaan/hello:1.0.1 .
docker run --rm -it -e "PAYLOAD_FILE=hello.payload.json" -e "YOUR_ENV_VAR=ANYTHING" mistobaan/hello:0.0.1
docker push mistobaan/hello:0.0.1

