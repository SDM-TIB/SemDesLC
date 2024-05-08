#!/bin/bash

RUNS=10

DOCKER_KG_LC="kg_lc"
DOCKER_KG_SEMDESLC="kg_semdeslc"
DOCKER_ENGINE_FEDX="fedx"
DOCKER_ENGINE_DETRUSTY="detrusty"
DOCKER_ENGINE_ANAPSID="anapsid"

docker-compose down > /dev/null 2> /dev/null
docker-compose up -d $DOCKER_KG_LC $DOCKER_KG_SEMDESLC > /dev/null 2> /dev/null
sleep 60s  # give some time to Virtuoso to be responsive

start_engine() {
  docker-compose up -d $1 > /dev/null 2> /dev/null
  sleep 2s
}

stop_engine() {
  docker stop $1 > /dev/null 2> /dev/null
}

for ((i=1;i<=RUNS;i++)); do
  for query_file in $(echo "./sparql/queries/*.sparql"); do
    query_file=${query_file: 1}
    query_file_name=$(basename -- "$query_file")
    query_id=${query_file_name%.*}
    query_id=${query_id/-/.}

    docker restart $DOCKER_KG_LC $DOCKER_KG_SEMDESLC > /dev/null 2> /dev/null
    sleep 60s

    start_engine $DOCKER_ENGINE_DETRUSTY
    echo "$i. Running DeTrusty for $query_id"
    docker exec -it $DOCKER_ENGINE_DETRUSTY bash -c "timeout 600 ./run.sh $query_id >> /results/detrusty.csv"
    stop_engine $DOCKER_ENGINE_DETRUSTY

    docker restart $DOCKER_KG_LC $DOCKER_KG_SEMDESLC > /dev/null 2> /dev/null
    sleep 60s

    start_engine $DOCKER_ENGINE_FEDX
    echo "$i. Running FedX for $query_id"
    docker exec -it $DOCKER_ENGINE_FEDX bash -c "timeout 600 ./run.sh $query_id >> /results/fedx.csv"
    stop_engine $DOCKER_ENGINE_FEDX

    docker restart $DOCKER_KG_LC $DOCKER_KG_SEMDESLC > /dev/null 2> /dev/null
    sleep 60s

    start_engine $DOCKER_ENGINE_ANAPSID
    echo "$i. Running ANAPSID for $query_id"
    docker exec -it $DOCKER_ENGINE_ANAPSID bash -c "timeout 600 ./run.sh $query_id >> /results/anapsid.csv"
    stop_engine $DOCKER_ENGINE_ANAPSID
  done
done

docker-compose down > /dev/null 2> /dev/null

# Clean up the result files
sed -i '/^Q/!d' results/querying/anapsid.csv
sed -i '/^Q/!d' results/querying/detrusty.csv
sed -i '/^Q/!d' results/querying/fedx.csv
