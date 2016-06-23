FROM ubuntu:16.04

RUN apt-get update && apt-get install --yes python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install click
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install --yes apt-utils
RUN apt-get -f --yes install

RUN mkdir /stuffer
COPY . /stuffer
WORKDIR /stuffer
