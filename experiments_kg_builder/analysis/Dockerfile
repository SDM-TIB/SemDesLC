FROM python:3.12.3-slim-bullseye

COPY . /app
RUN apt-get update &&\
    apt-get install -y --no-install-recommends texlive-full &&\
    apt-get clean &&\
    pip install --no-cache -r /app/requirements.txt

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
