docker run -u 0 -v ~/repos/adeb/:/home/$USER/adeb \
          --net=host  ubuntu_adeb \
          bash -c " \
                  cd adeb && \
                  sudo chmod o+r /tmp/ &&\
                  sudo ln -s $(pwd)/adeb /usr/bin/adeb  &&\
                  ./adeb prepare --bcc --build --arch amd64 \
                  "