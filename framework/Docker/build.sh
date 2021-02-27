# bash
export uid=$(id -u)
export gid=$(id -g)
docker build --build-arg USER=$USER \
             --build-arg UID=$uid \
             --build-arg GID=$gid \
             --build-arg PW=1111 \
             -t ubuntu_aosp_usr \
             -f Dockerfile\
             .
