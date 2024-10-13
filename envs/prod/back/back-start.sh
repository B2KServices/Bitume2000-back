#!/bin/bash

source /code/envs/shared/back/back-start-shared.sh

uwsgi --enable-threads --ini app/uwsgi.ini
