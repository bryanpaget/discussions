#!/usr/bin/env bash 

virtualenv venv --python=python3

venv/bin/pip install -r requirements.txt

python -m spacy download en_core_web_sm