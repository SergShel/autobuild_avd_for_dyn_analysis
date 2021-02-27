import os
import subprocess
import getpass

class AdebManager:
    def __init__(self):
        self.arch = 'amd64'
        self.repo_url = 'https://github.com/joelagnel/adeb'
        self.repos_path = '/home/' + getpass.getuser() + '/repos'
        self.adeb_repo_path = self.repos_path + '/adeb/'

    def clone_repo(self):
        if (not os.path.exists(self.repos_path)):
            os.mkdir(self.repos_path)

        wd = os.getcwd()
        os.chdir(self.repos_path)
        subprocess.call(('git clone ' + self.repo_url), shell=True)
        os.chdir(wd)

    def install_adeb(self):
        wd = os.getcwd()
        os.chdir(self.adeb_repo_path)

        subprocess.call(('adb root'), shell=True)

        # subprocess.call((f'sh ./adeb prepare --full --build --arch {self.arch}'), shell=True)


        os.chdir('/home/' + getpass.getuser() + '/Desktop/emulator-setup')
        subprocess.call(('sh ~/Desktop/emulator-setup/install-adeb-and-bcc.sh'), shell=True)


        os.chdir(wd)

    def create_ubuntu_container(self):
        framework_dir = os.getcwd()

        os.chdir(framework_dir + '/adeb_Docker')
        rc = subprocess.run("sh build.sh", shell=True, text=True)
        print(rc.stdout)

        os.chdir(framework_dir)

    def run_ubuntu_container(self):
        wd = os.getcwd()
        os.chdir('./adeb_Docker')
        rc = subprocess.run("chmod 755 run_container.sh && ./run_container.sh", shell=True, text=True)

        os.chdir(wd)

    def postinstall_setup(self):
        wd = os.getcwd()
        os.chdir(self.adeb_repo_path)
        subprocess.run("./adeb shell chmod o+r /etc/resolv.conf", shell=True, text=True)
        subprocess.run("./adeb push adeb_util/solve-bcc-hardcoded-path.sh", shell=True, text=True)
        subprocess.run("./adeb shell ./solve-bcc-hardcoded-path.sh", shell=True, text=True)
        subprocess.run("./adeb shell ./bcc-master/build-bcc.sh", shell=True, text=True)
        subprocess.run("./adeb shell apt update", shell=True, text=True)
        subprocess.run("./adeb shell apt upgrade", shell=True, text=True)
        subprocess.run("./adeb shell apt-get install -y python git nano linux-perf trace-cmd \
                                                strace rt-app xz-utils clang-7 gcc libtool \
                                                autoconf make cmake python3-pip fish bpfcc-tools", shell=True, text=True)
        subprocess.run("./adeb shell pip3 install filemagic", shell=True, text=True)


        os.chdir(wd)
