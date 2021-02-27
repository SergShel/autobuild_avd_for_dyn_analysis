#!/bin/bash

cd ~/repos/aosp
. ./build/envsetup.sh
lunch "$1"

emulator -selinux permissive -show-kernel -no-snapshot \
 -kernel ~/repos/kernel_source/goldfish/arch/x86/boot/bzImage &
