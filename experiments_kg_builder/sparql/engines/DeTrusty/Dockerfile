FROM python:3.12.3-slim-bullseye

COPY run.py /app/run.py
COPY run.sh /app/run.sh
COPY rdfmts.json /app/rdfmts.json
RUN chmod +x /app/run.sh &&\
    pip install --no-cache DeTrusty==0.15.6 certifi==2024.2.2 charset-normalizer==3.3.2 idna==3.7 isodate==0.6.1 ply==3.11 pyparsing==3.1.2 python-dateutil==2.9.0.post0 rdflib==7.0.0 requests==2.31.0 six==1.16.0 urllib3==2.2.1

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
