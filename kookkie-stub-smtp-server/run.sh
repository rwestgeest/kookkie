#!/bin/sh
. venv/bin/activate
pip install -r requirements.txt --user
python smtp-server.py
