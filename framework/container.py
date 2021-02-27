import os
import getpass
import subprocess


def create_ubuntu_container():
    current_host_user = getpass.getuser()
    framework_dir = os.getcwd()
    print("Current working directory: {0}".format(framework_dir))

    aosp_dir = "/home/"+ current_host_user + "aosp"
    os.chdir(framework_dir + '/Docker')
    rc = subprocess.run("./build.sh", shell=True, text=True)
    print(rc.stdout)

    os.chdir(framework_dir)
    return

def run_ubuntu_container():

    wd = os.getcwd()
    os.chdir('./Docker')
    rc = subprocess.run("./run_container.sh", shell=True, text=True)
    print(rc.stdout)

    os.chdir(wd)
    return

# create_ubuntu_container()
# run_ubuntu_container()