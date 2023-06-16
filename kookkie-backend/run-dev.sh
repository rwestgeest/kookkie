#!/bin/sh
set -e 
#. venv/bin/activate
export PATH=.local/bin/:$PATH
pip install --upgrade pip
pip install -r requirements.txt --user

. ./run.sh
