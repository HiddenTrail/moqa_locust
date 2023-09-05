#!/bin/bash
set -eo pipefail

DATE=$(date +"%Y-%m-%d_%H-%M")
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
locust_file=""
docker=false
test_env="test"
locust_container_image_name="moqa_locust:latest"
preserve_results=false
log_level="INFO"
results_path="testresults/${DATE}"

cd $SCRIPT_DIR

function shut_down() {
    echo "Removing old container"
    docker-compose down
}

function run_docker() {
  local existing_container=$(docker ps -aq --filter ancestor=${locust_container_image_name})
  if [ ! -z "${existing_container}" ] ; then
    shut_down
  fi
  mkdir -p ${results_path} && docker-compose up
}

function run_locust() {
  echo "Using environment: ${test_env}"
  export TEST_ENV=${test_env}
  if $docker ; then
    export LOCUSTFILE=${locust_file}; export BASE_URL=${base_url}; export LOG_LEVEL=${log_level}
    export LOG_FILE_M="${results_path}/master_logfile.log"; export LOG_FILE_W="${results_path}/worker_logfile.log"
    echo "Running using docker"
    run_docker
  else
    echo "Running using local locust"
    mkdir -p ${results_path}
    locust -f ${locust_file} -H ${base_url} \
        --loglevel ${log_level} --logfile ${results_path}/logfile.log
  fi
}

function delete_results() {
  if ! $preserve_results ; then
    echo "Removing testresults folder ${SCRIPT_DIR}/testresults"
    rm -rf testresults
  fi
}

while getopts "f:u:e:dpl:sh" opt; do
  case ${opt} in
    f )
      locust_file="${OPTARG}"
      ;;
    u )
      base_url="${OPTARG}"
      ;;
    e )
      test_env="${OPTARG}"
      ;;
    d )
      docker=true
      ;;
    p )
      preserve_results=true
      ;;
    l )
      log_level="${OPTARG}"
      ;;
    s )
      shut_down
      exit 0
      ;;
    \? )
      echo "Invalid Option -${OPTARG}" >&2
      exit 1
      ;;
    : )
      echo "Option ${OPTARG} requires an argument" >&2
      exit 1
      ;;
    h|* )
      echo "Usage:"
      echo "-f    LOCUSTFILE path, e.g. './locustfiles/login_and_auth.py'. Mandatory option."
      echo "-u    BASE URL. Mandatory option."
      echo "-e    Environment, e.g. 'test'. Default ${test_env}"
      echo "-d    Use docker for running locust"
      echo "-p    Preserve results from earlier runs. Default ${preserve_results}."
      echo "-l    Log level. Default is ${log_level}."
      echo "-s    Shut down docker containers."
      echo "-h    Help"
      exit 0
      ;;
    esac
done

delete_results
run_locust
