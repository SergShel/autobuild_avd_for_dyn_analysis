docker run  -v ~/repos/aosp/:/home/$USER/aosp -p 5000:80 ubuntu_aosp_usr bash -c "cd aosp && source build/envsetup.sh && lunch aosp_x86_64-eng && m"

