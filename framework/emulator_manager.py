import os
import subprocess
import getpass
import time

class EmuManager:
    def __init__(self, arch='x86_64'):
        self.arch = arch
        self.lang = 'eng'
        self.repo_path = '/home/' + getpass.getuser() + '/aosp'


    def start_emu(self):
        if (not os.path.exists(self.repo_path)):
            print('AOSP directiry is not found!!!')
            return

        # todo write another checks if the Avd for such architecture exists

        subprocess.call(("./emu_starter.sh aosp_" + self.arch + "-eng"), shell=True)
        time.sleep(25)    # waiting when emulator will be ready
