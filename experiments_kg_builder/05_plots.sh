#!/bin/bash

DOCKER_ANALYSIS="analysis"

docker-compose up -d --build $DOCKER_ANALYSIS # > /dev/null 2> /dev/null
docker exec -it $DOCKER_ANALYSIS bash -c "python plots_validation.py"
docker exec -it $DOCKER_ANALYSIS bash -c "python plots_querying.py"
docker exec -it $DOCKER_ANALYSIS bash -c "python box_plot.py"