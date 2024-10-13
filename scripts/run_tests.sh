#!/usr/bin/env bash

function show_usage() {
    echo -e "USAGE: bash run_tests.sh [-r pytest_results_directory] [--flask-mount-point path/to/project/files]"
    echo -e "-r, --results-dir      Chemin ou seront stockés les résultats du test"
    echo -e "--flask-mount-point    Chemin vers le dossier contenant le projet. Utile pour résoudre la problématique de docker:dind"\
            "et ses volumes dans Gitlab CI. Cf: https://gitlab.com/gitlab-org/gitlab-foss/-/issues/41227)"
}

VALID_ARGS=$(getopt -o r:h --long results-dir,help,flask-mount-point -- "$@")
if [[ $? -ne 0 ]]; then
    show_usage
    exit 1;
fi

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

#eval set -- "$VALID_ARGS"
while [ $# -gt 0 ]; do
  case "$1" in
    -r | --results-dir)
      export PYTEST_RESULT_DIR=$2
      shift
      ;;
    --flask-mount-point)
      export FLASK_MOUNT_POINT=$2
      echo $FLASK_MOUNT_POINT
      shift
      ;;
    -h | --help)
        show_usage
        exit 0
        ;;
  esac
  shift
done

export SET_ENV_TO_TEST=1

echo $FLASK_MOUNT_POINT
docker-compose -f "$SCRIPT_DIR/../envs/dev/docker-compose.yml" up --attach flask
