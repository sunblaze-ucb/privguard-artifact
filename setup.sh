#!/bin/bash

python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PRIVGUARD=$(pwd)
