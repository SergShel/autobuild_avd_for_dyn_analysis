docker run  -v ~/repos/kernel_source:/home/$USER/kernel_source -p 5005:81 ubuntu_aosp_usr \
bash -c "cd kernel_source && \
          BUILD_CONFIG=goldfish/build.config.goldfish.x86_64 build/build.sh && \
          cd goldfish && \
          export ARCH=x86_64 && \
          make x86_64_ranchu_defconfig && \
          make prepare && make scripts && \
          make && \
        echo 'New Kernel and Kernel Modules are ready for usage :)' "

