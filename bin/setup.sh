#!/bin/bash

python3.11 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
