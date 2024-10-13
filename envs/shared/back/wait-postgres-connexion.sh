source envs/shared/back/check-db-var-with-prefix.sh

wait_postgres_connexion() {
  prefix=$1

  check_db_var_with_prefix "$prefix"
  if [[ $? -ne 0 ]]; then
    exit $?
  fi

  name="$prefix"_NAME
  ip="$prefix"_IP
  port="$prefix"_PORT
  user="$prefix"_USER

  pg_isready -d ${!name} -h ${!ip} -p ${!port} -U ${!user}
  while [[ $? -ne 0 ]] ; do
    echo "Waiting for postgres server to be ready to accept connections..."
    sleep 2
    pg_isready -d ${!name} -h ${!ip} -p ${!port} -U ${!user}
  done

  echo "Postgres server ready to accept connections"
}

