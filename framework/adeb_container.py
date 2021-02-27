import subprocess
import os
import getpass


def create_ubuntu_container():
    framework_dir = os.getcwd()

    aosp_dir = "~/repos/adeb"
    os.chdir(framework_dir + '/adeb_Docker')
    rc = subprocess.run("sh build.sh", shell=True, text=True)
    print(rc.stdout)

    os.chdir(framework_dir)
