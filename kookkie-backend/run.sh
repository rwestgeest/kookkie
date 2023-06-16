#!/bin/sh
set -e 
waitress-serve  --port 5000 --call 'boot:main'
