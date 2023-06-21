#!/bin/bash
export CURRENT_UID=$(id -u ${USER})
export CURRENT_GID=$(id -g ${USER})

if [[ "$1" == "" ]] 
then
  echo usage $0 stubbed-backend
  exit 1
fi

docker-compose -f $1 up
