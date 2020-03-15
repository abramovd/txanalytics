#!/usr/bin/env bash

export CUSTOM_COMPILE_COMMAND='./compile_requirements.sh'

pip-compile --no-index requirements/api/main.in $1 $2 $3
pip-compile --no-index requirements/api/test.in $1 $2 $3
pip-compile --no-index requirements/datagenerator/main.in $1 $2 $3
pip-compile --no-index requirements/notebook/main.in $1 $2 $3
