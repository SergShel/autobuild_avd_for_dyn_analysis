# We start with our base OS, Ubuntu 20.04 with Ubuntu 18.04 adeb works incorrect
FROM ubuntu:latest

MAINTAINER Siarhei Sheludzko


RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install apt-utils

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update

RUN apt-get -y install python python3 adb sudo python3-pip 

RUN pip3 install frida-tools

ARG USER=docker
ARG UID=1000
ARG GID=1000
# default password for user

RUN useradd -m ${USER} --uid=${UID} 
# Setup default user, when enter docker container
USER ${UID}:${GID}
WORKDIR /home/${USER}
