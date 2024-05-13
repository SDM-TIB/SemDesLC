#!/bin/bash

DOCKER_MYSQL="mysql"
DOCKER_RDFIZER="sdmrdfizer"

docker build -f ./morph-kgc/Dockerfile -t morph-kgc --build-arg optional_dependencies="mysql" .
docker-compose down > /dev/null 2> /dev/null
docker-compose up -d $DOCKER_MYSQL $DOCKER_KG_SEMDESLC > /dev/null 2> /dev/null
sleep 60s # give some time to MySQL server to be responsive

num_executions=10

echo "Measuring Execution Time"
echo "-------------------------------------"
echo "SDM-RDFizer" > time_output.txt
echo "SDM-RDFizer"
for (( i=1; i<=$num_executions; i++ ))
do
    echo "Execution $i:"
    { time docker exec -it sdmrdfizer python3 -m rdfizer -c /data/configfile-syntheticDB.ini; } 2>&1 | grep real | awk '{print $2}' >> time_output.txt
    echo "-------------------------------------"
done

echo "Morph-KGC" >> time_output.txt
echo "Morph-KGC"
for (( i=1; i<=$num_executions; i++ ))
do
    echo "Execution $i:"
    { time docker run -it --name morph-kgc_interpretme --network experiments_docker_file_experiment  -v $(pwd)/morph-kgc:/app/files morph-kgc files/morph.ini; } 2>&1 | grep real | awk '{print $2}' >> time_output.txt
    echo "-------------------------------------"
    docker rm morph-kgc_interpretme
done

echo "RMLMapper" >> time_output.txt
echo "RMLMapper"
for (( i=1; i<=$num_executions; i++ ))
do
    echo "Execution $i:"
    { time docker run --name rmlmapper_interpretme --network experiments_docker_file_experiment -v $(pwd)/Mappings_SyntheticDB:/data rmlio/rmlmapper-java:v6.0.0 -m LC-mappings.ttl -d; } 2>&1 | grep real | awk '{print $2}' >> time_output.txt
    echo "-------------------------------------"
    docker rm rmlmapper_interpretme
done

echo "Measuring Memory Usage"
echo "-------------------------------------"
echo "SDM-RDFizer" > memory_output.txt
echo "SDM-RDFizer"
for (( i=1; i<=$num_executions; i++ ))
do
    echo "Execution $i:"
    docker exec -i sdmrdfizer python3 -m rdfizer -c /data/configfile-syntheticDB.ini & sleep 7 && docker stats --no-stream sdmrdfizer --format "{{.MemUsage}}" | awk '{print $1}' >> memory_output.txt
    echo "-------------------------------------"
done

echo "Morph-KGC" >> memory_output.txt
echo "Morph-KGC"
for (( i=1; i<=$num_executions; i++ ))
do
    echo "Execution $i:"
    docker run -i --name morph-kgc_interpretme --network experiments_docker_file_experiment  -v $(pwd)/morph-kgc:/app/files morph-kgc files/morph.ini & sleep 5 && docker stats --no-stream morph-kgc_interpretme --format "{{.MemUsage}}" | awk '{print $1}'  >> memory_output.txt & wait && docker rm morph-kgc_interpretme
    echo "-------------------------------------"
done

echo "RMLMapper" >> memory_output.txt
echo "RMLMapper"
for (( i=1; i<=$num_executions; i++ ))
do
    echo "Execution $i:"
    docker run --name rmlmapper_interpretme --network experiments_docker_file_experiment -v $(pwd)/Mappings_SyntheticDB:/data rmlio/rmlmapper-java:v6.0.0 -m LC-mappings.ttl -d > output.nt & sleep 250 && docker stats --no-stream rmlmapper_interpretme --format "{{.MemUsage}}" | awk '{print $1}' >> memory_output.txt & wait && docker rm rmlmapper_interpretme
    echo "-------------------------------------"
done

docker-compose down > /dev/null 2> /dev/null