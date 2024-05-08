# Use a base image with Java pre-installed
FROM openjdk:11

RUN apt-get update &&\
    apt-get install -y python3 python3-pip &&\
    apt-get clean &&\
    pip3 install rdflib pandas==2.1.3

# Set the working directory inside the container
WORKDIR /Rules

# Copy the JAR file into the container
COPY ./Rules/amie3.jar /Rules/amie3.jar
COPY ./process.py /Rules/process.py
COPY ./genRules.py /Rules/genRules.py
COPY ./run.sh /Rules/run.sh

RUN chmod +x /Rules/run.sh

# Command to run the application when the container starts
#CMD ["python", "process.py", "/Rules/data/LungCancer.nt", "/Rules/data/LungCancer.tsv"]
CMD ["bash", "-c", "/Rules/run.sh"]