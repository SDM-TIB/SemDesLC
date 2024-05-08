FROM ubuntu:18.04

COPY . /app

RUN apt-get update &&\
    apt-get install -y --no-install-recommends openjdk-8-jre-headless redir &&\
    apt-get autoremove -y openjdk-11-jre* &&\
    apt-get clean &&\
    chmod +x /app/run.sh

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
