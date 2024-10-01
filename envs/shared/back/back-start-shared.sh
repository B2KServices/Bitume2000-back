#!/bin/bash

source /code/envs/shared/back/wait-mongo-connexion.sh
source /code/envs/shared/back/wait-postgres-connexion.sh

wait_postgres_connexion DB
