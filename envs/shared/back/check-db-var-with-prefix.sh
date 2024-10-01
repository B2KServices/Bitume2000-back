#!/bin/bash

check_db_var_with_prefix() (
  prefix=$1

  all_missing_env_vars=()
  check_env_var() {
    var_value=$(printf '%s\n' "${!1}")
    if [ -z $var_value ]; then
      all_missing_env_vars+=( $1 )
    fi
  }

  check_env_var "$prefix"_USER
  check_env_var "$prefix"_NAME
  check_env_var "$prefix"_IP
  check_env_var "$prefix"_PORT

  if [ ${#all_missing_env_vars[@]} -ne 0 ]; then
      echo "Missing environment variables: $all_missing_env_vars"
      exit 1
  fi
)