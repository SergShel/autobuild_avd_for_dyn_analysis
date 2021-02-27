#!/bin/bash

cd ~/aosp 
. ./build/envsetup.sh
lunch "$1"

emulator -selinux permissive -writable-system -show-kernel -no-snapshot -wipe-data \
 -kernel ~/repos/kernel_source/goldfish/arch/x86_64/boot/bzImage &
