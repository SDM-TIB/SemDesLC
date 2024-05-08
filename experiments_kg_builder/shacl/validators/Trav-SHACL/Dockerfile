FROM python:3.12.3-slim-bullseye

COPY run.py /app/run.py
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh &&\
    pip install --no-cache pip==24.0 SPARQLWrapper==2.0.0 isodate==0.6.1 pyparsing==3.1.2 rdflib==7.0.0 six==1.16.0 TravSHACL==1.7.1

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
