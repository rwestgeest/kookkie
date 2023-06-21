#!/bin/bash
set -e 

cd ./kookkie-backend
./build.sh $@
cd -
cd ./kookkie-frontend
./build.sh $@
cd -
cd ./kookkie-proxy
./build.sh $@
cd -
# cd ./kookkie-backup
# ./build.sh $@
# cd -
# cd ./kookkie-cloudwatch-agent
# ./build.sh $@
# cd -

