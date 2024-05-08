#!/bin/bash

docker-compose up -d --build
sleep 120s  # give some time to the containers for initialization
docker-compose down
