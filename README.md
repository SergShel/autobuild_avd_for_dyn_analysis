# autobuild_avd_for_dyn_analysis
Source Code for Bachelor-Thesis "Entwicklung eines Build-Systems für Android Virtual Devices für Sicherheitsforscher"

This project is made for Linux OS only and was tested on Manjaro OS (Kernel 5.4)
For compiling of AOSP, Android Kernel and Magisk you need at least 16Gb RAM, more is better. For downloading of AOSP-, Android-Kernel-, Magisk- and adeb- Repositories and saving the builds of them you need at least 300 Gib free space on hard drive. 

Dependencies:
python
docker-ce docker-ce-cli containerd.io
git-core gnupg flex bison build-essential zip curl zlib1g-dev gcc-multilib g++-multilib libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig

You have to install command line tools from here https://developer.android.com/studio/#downloads 
Alternatively you can install them as part of Android Studio (same link)

To start the Build of AVD: python framework/main.py
This will:
  *init and sync AOSP-Repo (branch='android-10.0.0_r41') in ~/repos/aosp
  *create Docker-Container for compiling of AOSP and Kernel
  *compile AOSP in Container
  *init and sync Kernel-Repo (branch='q-goldfish-android-goldfish-4.14-dev') in ~/repos/kernel_source
  *save "hello-world"-Kernel module source code in Kernel-Repo and set the configs
  *compile kernel and "hello-world"-kernel module in Container
  *start AVD
  *push of hello.ko (compiled kernel module) to /data/ on AVD
  *clone Magisk Repo
  *set config to build Magisk
  *build NDK
  *build Magisk and MagiskManager
  *install Magisk and MagiskManager on AVD
  *start Magisk-Daemon
  *find the latest version of Frida server for Android x86_64 on the release page and download it
  *install frida_server on AVD
  *clone adeb repo
  *create Docker container for building rootfs of adeb
  *build adeb rootfs in container and install it on AVD
  *install neccessary dependencies inside of adeb and build BCC there (!!! in actual implementation the compiling of bcc works incorrect. It will be fixed!!!)
  
!!!Important Note!!! This command will go through all steps of build process. If you need only some of them, you have to comment/uncomment some lines in main.py
This project is a prototype of build-System and there is no flexible UI for selecting of Android-, Kernel-, Magisk- Versions.  
