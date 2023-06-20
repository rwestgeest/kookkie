#!/bin/bash
set -e
VERSION=$(cat VERSION)
REPO="525595969507.dkr.ecr.eu-central-1.amazonaws.com/qwan/afdop-backend"

command=$1
case $command in
  push)
    docker push $REPO:$VERSION
    ;;
  *)
    rm -r venv
    python -m venv venv
    . venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt -r dev-requirements.txt
    mypy boot.py app tests
    ./run_tests.sh
    docker build . -t $REPO:$VERSION
    ;;
esac
