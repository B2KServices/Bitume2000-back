source envs/shared/back/check-db-var-with-prefix.sh

wait_mongo_connexion() {
  prefix=$1

  check_db_var_with_prefix "$prefix"
  if [[ $? -ne 0 ]]; then
    exit $?
  fi
  ip="$prefix"_IP
  port="$prefix"_PORT


  echo "Attente de MongoDB sur ${!ip}:${!port}..."
  while ! nc -z ${!ip} ${!port}; do
    sleep 1
  done

  echo "MongoDB server ready to accept connections"
}