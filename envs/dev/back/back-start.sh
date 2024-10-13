#!/bin/bash

source ./envs/shared/back/back-start-shared.sh

if [ $SET_ENV_TO_TEST == 1 ]; then
    export ENV=test
    mkdir -p /tmp/.pytest_cache
    if [ -z "$PYTEST_RESULT_DIR" ]; then
      PYTEST_RESULT_DIR=./.pytest-results
    fi
    mkdir -p $PYTEST_RESULT_DIR
    pytest -s -o cache_dir=/tmp/.pytest_cache --junitxml="$PYTEST_RESULT_DIR/report.xml"
    pytest -s -o cache_dir=/tmp/.pytest_cache --cov --cov-report term --cov-report xml:"$PYTEST_RESULT_DIR/coverage.xml" --cov-report html:"$PYTEST_RESULT_DIR/coverage.html"
    exit $?
else
    python app/main.py
fi

