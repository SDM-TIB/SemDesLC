FROM ubuntu:18.04

RUN apt-get update &&\
    apt-get install -y openjdk-11-jre-headless git curl gnupg2 redir &&\
    echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list &&\
    echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | tee /etc/apt/sources.list.d/sbt_old.list &&\
    curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add &&\
    apt-get update &&\
    apt-get install -y sbt &&\
    apt-get clean &&\
    git clone https://github.com/weso/shaclex.git /app &&\
    cd /app &&\
    git checkout 821b7eb &&\
    sbt test

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
