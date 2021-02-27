#!/bin/bash
export uid=$(id -u)
export gid=$(id -g)

docker build --build-arg USER=$USER \
        --build-arg UID=$uid \
        --build-arg GID=$gid \
        -t ubuntu_frida \
        -f Dockerfile .
