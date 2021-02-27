# We start with our base OS, Ubuntu 18.04
FROM ubuntu:18.04

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



#RUN apt-get -qq update
#RUN apt-get -qqy upgrade
RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt-get -y install adb bc bison build-essential curl debootstrap flex fontconfig gcc-multilib \
			 git-core g++-multilib gnupg lib32ncurses5-dev lib32z1-dev libc6-dev-i386 \
			 libgl1-mesa-dev libx11-dev libxml2-utils openjdk-8-jdk openjdk-8-jre python \
			 python3 qemu-user-static repo rsync sudo unzip vim wget x11proto-core-dev \
			 xsltproc zip zlib1g-dev
ARG USER=docker
ARG UID=1000
ARG GID=1000
# default password for user
ARG PW=docker

RUN useradd -m ${USER} --uid=${UID} && echo "${USER}:${PW}" | \
      chpasswd

# Setup default user, when enter docker container
USER ${UID}:${GID}
WORKDIR /home/${USER}
