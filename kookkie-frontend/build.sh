#!/bin/bash
set -e

VERSION=$(cat VERSION)
REPO="525595969507.dkr.ecr.eu-central-1.amazonaws.com/qwan/kookkie-frontend"

command=$1
case $command in
  push)
    docker push $REPO:"$VERSION"
    ;;
  *)
    npm install
    npm run test
    rm -r deploy/dist || echo ''
    rm -r dist || echo ''
    mkdir dist
    cp -a index.html dist/
    cp -a app dist/
    mv dist deploy
    docker build deploy -t $REPO:"$VERSION"
    ;;
esac