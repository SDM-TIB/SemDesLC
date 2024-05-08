#FROM python:2.7.18-stretch
FROM ubuntu:16.04

RUN apt-get update &&\
    apt-get install -y git &&\
    apt-get install -y --no-install-recommends python2.7 python-pip python-setuptools &&\
    apt-get clean &&\
    git clone https://github.com/SDM-TIB/anapsid.git /app &&\
    cd /app &&\
    git checkout decd9ef &&\
    pip install --no-cache-dir -r requirements.txt &&\
    python setup.py install

COPY federation.txt /app/federation.txt
COPY run.py /app/run.py
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
