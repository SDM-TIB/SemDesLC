FROM ubuntu:18.04

RUN apt-get update &&\
    apt-get install -y openjdk-8-jre-headless wget &&\
    apt-get autoremove -y openjdk-11-jre* &&\
    apt-get clean &&\
    mkdir /app &&\
    cd /app &&\
    wget https://github.com/rdfshapes/shacl-sparql/releases/download/v1.0-alpha.1/valid-1.0-SNAPSHOT.jar

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
