import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import os
import subprocess

class FridaManager:
    def __init__(self, architecture):
        self.arch = architecture
        self.releases_url = 'https://github.com/frida/frida/releases'
        self.download_url, self.f_server_name = self.__get_url_and_name(architecture)
        self.folder_path = "./frida_server/"

    def __get_url_and_name(self, arch: str):
        """
        Private method for finding of download url and name of last version of frida server for android
        :param arch: string of architecture
        :return: download url of last version of frida server for android with specified architecture
        """
        page = requests.get(self.releases_url)
        page_text = page.text
        soup = BeautifulSoup(page_text, features="html.parser")
        regex = re.compile('frida-server-[0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2}-android-' + arch, re.IGNORECASE)
        frida_server_name = soup.find(text=regex)[0:-3]
        release_version = re.findall("[0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2}", frida_server_name)[0]
        return (self.releases_url + '/download/' + release_version + '/' + frida_server_name + ".xz"), frida_server_name

    def download_frida_server(self):
        # create folder frida_server if not exist
        if (not os.path.exists(self.folder_path)):
            os.mkdir(self.folder_path)

        # retrieving data from the URL using get method
        r = requests.get(self.download_url)

        # giving a name and saving it in any required format
        # opening the file in write mode
        with open(self.folder_path + self.f_server_name + '.xz', 'wb') as f:
            # writes the URL contents from the server
            f.write(r.content)
        print('Archive ' + self.f_server_name + '.xz was successfully downloaded.')

    def get_server_name(self):
        return self.f_server_name

    def extract_archive(self):
        if(os.path.exists(self.folder_path + self.f_server_name)):
            os.remove(self.folder_path + self.f_server_name)
        rc = subprocess.run('unxz ' + self.folder_path + self.f_server_name + '.xz', shell=True, stdout=subprocess.PIPE, text=True)
        print('Archive is extracted. Path to frida-server: ' + self.folder_path + self.f_server_name)
