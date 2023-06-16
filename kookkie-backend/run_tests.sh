#!/bin/bash

export PYTHONPATH=tests:. 
. venv/bin/activate

if [[ "$1" == "watch" ]]
then
   shift
   pytest-watch -- --disable-pytest-warnings  --full-trace $@
else
   pytest --disable-pytest-warnings --junitxml=reports/test-report.xml $@
fi
