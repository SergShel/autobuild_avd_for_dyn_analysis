import multiprocessing
import os
import subprocess
import getpass
import sys


class RepoManager:
    def __init__(self, branch='android-10.0.0_r41'):
        self.repo_url = 'https://android.googlesource.com/platform/manifest'
        self.branch = branch
        self.threadcount = multiprocessing.cpu_count() * 2
        self.repo_path = '/home/' + getpass.getuser() + '/aosp'


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

        subprocess.call(('repo', 'sync', '-j', str(self.threadcount)), stdout=sys.stdout)

        os.chdir(wd)

    def repo_init(self):
        if (not os.path.exists(self.repo_path)):
            os.mkdir(self.repo_path)

        wd = os.getcwd()
        os.chdir(self.repo_path)
        print("Initialisation of AOSP Repository (" + self.branch + ")" )
        subprocess.call(['repo', 'init', '-u', self.repo_url, '-b', self.branch])

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
