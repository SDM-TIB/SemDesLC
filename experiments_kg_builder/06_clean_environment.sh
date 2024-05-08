#!/bin/bash

docker-compose down -v
docker rmi mysql:8.0.19 prohde/virtuoso-opensource-7:7.2.11 semdeslc:travshacl semdeslc:shaclex semdeslc:shaclsparql semdeslc:detrusty semdeslc:fedx
chown -R $(logname):$(logname) ./results
