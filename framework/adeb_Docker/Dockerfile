# We start with our base OS, Ubuntu 20.04 with Ubuntu 18.04 adeb works incorrect
FROM ubuntu:20.04

MAINTAINER Siarhei Sheludzko


RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install apt-utils

# Add the repositories needed for the packages we're going to install
# These are added to the Ubuntu base, not your host operating system. As are all the packages.
#RUN echo "deb http://archive.ubuntu.com/ubuntu trusty multiverse" >> /etc/apt/sources.list
#RUN echo "deb-src http://archive.ubuntu.com/ubuntu trusty multiverse" >> /etc/apt/sources.list
#RUN echo "deb http://archive.ubuntu.com/ubuntu/ trusty-security multiverse" >> /etc/apt/sources.list
#RUN echo "deb-src http://archive.ubuntu.com/ubuntu/ trusty-security multiverse" >> /etc/apt/sources.list

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update

RUN apt-get -y install git-core gnupg flex bison build-essential zip curl zlib1g-dev gcc-multilib \
			g++-multilib libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev \ 
			lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig rsync python python3 \
			adb qemu-user-static debootstrap sudo

ARG USER=docker
ARG UID=1000
ARG GID=1000
# default password for user

RUN useradd -m ${USER} --uid=${UID} 
# Setup default user, when enter docker container
USER ${UID}:${GID}
WORKDIR /home/${USER}

