#!/bin/sh

VERSION=$(cat VERSION)
REPO="525595969507.dkr.ecr.eu-central-1.amazonaws.com/qwan/kookkie-proxy"

command=$1
case $command in
  push)
    docker push $REPO:$VERSION
    ;;
  *)
    docker build . -t $REPO:$VERSION
    ;;
esac