#!/bin/bash

RUNS=10

DOCKER_KG_LC="kg_lc"
DOCKER_ENGINE_SHACL2SPARQL="shaclsparql"
DOCKER_ENGINE_SHACLEX="shaclex"
DOCKER_ENGINE_TRAVSHACL="travshacl"

docker-compose down > /dev/null 2> /dev/null
docker-compose up -d $DOCKER_KG_LC > /dev/null 2> /dev/null
sleep 60s  # give some time to Virtuoso to be responsive

start_engine() {
  docker-compose up -d $1 > /dev/null 2> /dev/null
  sleep 2s
}

run_engine() {
  echo "Running $2"
  docker exec -it $1 bash -c "./run.sh >> /results/$2.csv"
}

stop_engine() {
  docker stop $1 > /dev/null 2> /dev/null
}

for ((i=1;i<=RUNS;i++)); do
  start_engine $DOCKER_ENGINE_SHACL2SPARQL
  run_engine $DOCKER_ENGINE_SHACL2SPARQL "SHACL2SPARQL"
  stop_engine $DOCKER_ENGINE_SHACL2SPARQL

  start_engine $DOCKER_ENGINE_SHACLEX
  run_engine $DOCKER_ENGINE_SHACLEX "shaclex"
  stop_engine $DOCKER_ENGINE_SHACLEX

  start_engine $DOCKER_ENGINE_TRAVSHACL
  run_engine $DOCKER_ENGINE_TRAVSHACL "Trav-SHACL"
  stop_engine $DOCKER_ENGINE_TRAVSHACL
done

docker-compose down > /dev/null 2> /dev/null
