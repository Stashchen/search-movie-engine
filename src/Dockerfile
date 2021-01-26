FROM ubuntu:20.04

# Initial update
RUN apt-get update -y && apt-get upgrade -y

# Installing python and its dependencies
RUN apt-get install -y wget python3.8 python3-pip libpq-dev

# Installing dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Create symbolik link to python
RUN ln -s /bin/python3.8 /bin/python

# Setup Project
WORKDIR /api

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .