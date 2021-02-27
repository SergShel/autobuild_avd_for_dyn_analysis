import multiprocessing
import os
import subprocess
import getpass
import sys

class MagiskManager():
    def __init__(self):
        self.repo_url = 'https://github.com/topjohnwu/Magisk.git'
        self.repos_path = '/home/' + getpass.getuser() + '/repos'
        self.magisk_repo_path = self.repos_path + '/Magisk/'
        self.config_sample_name = 'config.prop.sample'
        self.config_name = 'config.prop'
        # The version name and version code of Magisk
        self.version = '21.0'
        self.versionCode = '21000'
        # The version name and version code of Magisk Manager
        self.appVersion = '8.0.2'
        self.appVersionCode = '313'
        self.build_targets = ['ndk', 'all']

    def clone_repo(self):
        if (not os.path.exists(self.repos_path)):
            os.mkdir(self.repos_path)

        wd = os.getcwd()
        os.chdir(self.repos_path)
        subprocess.call(('git clone --recurse-submodules ' + self.repo_url), shell=True)
        os.chdir(wd)

    def set_config(self):

        with open(self.magisk_repo_path + self.config_sample_name, 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        # helper function
        def __insert_string(original_string: str, insertion: str):
            return original_string.split('\n')[0] + insertion + '\n'

        data[1] = __insert_string(data[1], self.version)
        data[2] = __insert_string(data[2], self.versionCode)
        data[5] = __insert_string(data[5], self.appVersion)
        data[6] = __insert_string(data[6], self.appVersionCode)

        # and write everything to conf.prop
        with open(self.magisk_repo_path + self.config_name, 'w') as file:
             file.writelines(data)

    def build_target(self, target: str):
        wd = os.getcwd()
        os.chdir(self.magisk_repo_path)
        subprocess.call(('python build.py' + target), shell=True)
        os.chdir(wd)

    def build_magisk(self):
        for target in self.build_targets:
            self.build_target(target)

    def install_magisk(self):
        wd = os.getcwd()
        os.chdir(self.magisk_repo_path + 'scripts')

        subprocess.call(('adb root'), shell=True)

        subprocess.call(('chmod 755 emulator.sh'), shell=True)
        subprocess.call(('./emulator.sh'), shell=True)
        subprocess.call(('adb shell "mkdir -p /data/adb/magisk"'), shell=True)
        subprocess.call(('adb shell "cp /data/local/tmp/busybox /data/adb/magisk/"'), shell=True)
        subprocess.call(('adb push util_functions.sh /data/adb/magisk/'), shell=True)
        self.start_magisk_deamon()

        os.chdir('../out')
        subprocess.call(('adb install app-debug.apk'), shell=True)
        os.chdir(wd)

    def start_magisk_deamon(self):
        subprocess.call(('adb shell sh /data/local/tmp/emulator.sh'), shell=True)







