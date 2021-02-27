import multiprocessing
import os, stat
import subprocess
import getpass
import sys
from distutils.dir_util import copy_tree

class KernelRepoManager:
    def __init__(self, branch='q-goldfish-android-goldfish-4.14-dev'):
        self.repo_url = 'https://android.googlesource.com/kernel/manifest'
        self.branch = branch
        self.threadcount = multiprocessing.cpu_count() * 2
        self.repo_path = '/home/' + getpass.getuser() + '/repos/kernel_source/'
        self.drivers_path = self.repo_path + 'goldfish/drivers/'
        self.kmodule_name = 'helloworld'
        self.kConfigPath = self.drivers_path + 'Kconfig'
        self.MakefilePath = self.drivers_path + 'Makefile'
        # self.defconfigPath = self.repo_path + 'goldfish/arch/x86/configs/x86_64_cuttlefish_defconfig'
        # self.defconfigPath = self.repo_path + 'goldfish/arch/x86/configs/x86_64_defconfig'
        self.defconfigPath = self.repo_path + 'goldfish/arch/x86/configs/x86_64_ranchu_defconfig'
        self.defconfigStrList = ['CONFIG_MODULES',
                                 'CONFIG_MODULE_FORCE_LOAD',
                                 'CONFIG_MODULE_UNLOAD',
                                 'CONFIG_MODULE_FORCE_UNLOAD']
        self.kConfigStr = 'source "drivers/' + self.kmodule_name + '/Kconfig"\n'
        self.MakefileStr = 'obj-$(CONFIG_HELLO_MOD) += ' + self.kmodule_name + '/\n'
        self.kmodule_path = self.repo_path + 'out/x86_64/goldfish/drivers/' + self.kmodule_name

    def repo_init(self):
        if (not os.path.exists(self.repo_path)):
            os.mkdir(self.repo_path)

        wd = os.getcwd()
        os.chdir(self.repo_path)
        print("Initialisation of Android Kernel Repository (" + self.branch + ")" )
        subprocess.call(['repo', 'init', '--depth=1', '-u', self.repo_url, '-b', self.branch])

        os.chdir(wd)

    def repo_sync(self):
        if (not os.path.exists(self.repo_path)):
            self.repo_init()
        current_rev = self.get_current_revision()

        if(current_rev not in self.branch):
            self.repo_init()

        wd = os.getcwd()
        os.chdir(self.repo_path)
        print("Syncronisation of Repository (" + self.branch + ")")
        print("It will take some time.")

        subprocess.call(('repo', 'sync', '-c', '--no-tags', '--no-clone-bundle', '-j', str(self.threadcount)), stdout=sys.stdout)

        os.chdir(wd)

    def get_current_revision(self):
        if (not os.path.exists(self.repo_path)):
            return None
        else:
            """
            shell pipeline:    repo info | grep 'Manifest revision' | uniq | cut -f3 -d'/'
            """
            wd = os.getcwd()
            os.chdir(self.repo_path)
            repo_info = subprocess.Popen(['repo', 'info'], stdout=subprocess.PIPE)
            manifest_revisions = subprocess.Popen(('grep', 'Manifest revision'), stdin=repo_info.stdout, stdout=subprocess.PIPE)
            manifest_revision = subprocess.Popen(('uniq'), stdin=manifest_revisions.stdout, stdout=subprocess.PIPE)
            revision_name = subprocess.check_output(('cut', '-f3', '-d', '/'), stdin=manifest_revision.stdout).decode("utf-8")[0:-1]
            os.chdir(wd)
            return revision_name

        return None

    def add_helloworld_ksource(self):
        wd = os.getcwd()
        copy_tree(wd + '/kernel_modules/' + self.kmodule_name, self.drivers_path + '/' + self.kmodule_name)

    def set_Kconfig(self):

        with open(self.kConfigPath, 'r') as file:
            # read a list of lines into data
            data = file.readlines()
            file.close()

        for line in data:
            #check if Kconfig was set earlier
            if line == self.kConfigStr:
                print("Configuration of drivers/Kconfig was done earlier. Changes are not necessary.")
                return

        data.insert(len(data)-1, self.kConfigStr + '\n')

        # and write everything to conf.prop
        with open(self.kConfigPath, 'w') as file:
             file.writelines(data)
             file.close()
        print("driver/Kconfig file was configured successfully.")

    def set_Makefile(self):

        with open(self.MakefilePath, 'r') as file:
            # read a list of lines into data
            data = file.readlines()
            file.close()

        for line in data:
            #check if Kconfig was set earlier
            if line == self.MakefileStr:
                print("Configuration of drivers/Makefile was done earlier. Changes are not necessary.")
                return

        data.append(self.MakefileStr)

        # and write everything to conf.prop
        with open(self.MakefilePath, 'w') as file:
             file.writelines(data)
             file.close()

        print("driver/Makefile was configured successfully.")

    def set_defconfig(self):

        def Diff(li1, li2):
            # Helper-function to find the difference of 2 lists
            return (list(list(set(li1) - set(li2)) + list(set(li2) - set(li1))))

        with open(self.defconfigPath, 'r') as file:
            # read a list of lines into data
            data = file.readlines()
            file.close()

        implemented_parameters = []

        for line in data:
            for conf_param in self.defconfigStrList:
                if line == conf_param + '=y\n':
                    print('Parameter ' + conf_param + ' was set earlier.')
                    implemented_parameters.append(conf_param)
        parameters_to_append = Diff(self.defconfigStrList, implemented_parameters)

        for param in parameters_to_append:
            data.append(param + '=y\n')

        with open(self.defconfigPath, 'w') as file:
             file.writelines(data)
             file.close()

        if not parameters_to_append:
            print("All necessary parameters are set earlier. Defconfig is ready for usage")
        else:
            print("Parameters [" + ', '.join(parameters_to_append) + '] were set to y')





    def compile_kernel(self):
        wd = os.getcwd()
        os.chmod(wd + '/Docker/run_container_kernel_build.sh', 0o755)   # chmod 755 /path/
        rc = subprocess.run('sh ' + wd + '/Docker/run_container_kernel_build.sh', shell=True, text=True)
        print(rc.stdout)
        os.chdir(wd)

    def push_module2emu(self):
        if (os.path.exists(self.kmodule_path + '/hello.ko')):
            os.chmod('./push_module2emu.sh', 0o755)  # chmod 755 /path/
            subprocess.call(('sh push_module2emu.sh ' + self.kmodule_path + '/hello.ko'), shell=True)
            # subprocess.run('adb push ' + self.kmodule_path + '/hello.ko' + ' /data/kernel_modules')
        else:
            print(self.kmodule_name + ' kernel module not found')


