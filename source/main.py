import core.service
import subprocess
import requests
import tarfile
import pathlib
import shutil
import json
import time
import os

class App:
    def __init__(self):
        self.menu = {
            'Main': core.service.Menu(
                self.piCraftText() + '\nMain menu',
                ['Servers', 'Settings', 'Destroy']
            ),
            'Servers': core.service.Menu(
                self.piCraftText() + '\nServers',
                list(self.getServers().keys())
            ),
            'Confirm': core.service.Menu(
                self.piCraftText() + '\nAre you sure?',
                ['I am sure', 'Nevermind']
            )
        }

        links = {
            'Java': 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jre_aarch64_linux_hotspot_17.0.8.1_1.tar.gz',
            'Vanilla':   {
                'Latest': 'https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba59902951553/server.jar'
            }, 'Paper':  {
                '1.20.1': 'https://api.papermc.io/v2/projects/paper/versions/1.20.1/builds/169/downloads/paper-1.20.1-169.jar',
                '1.19.4': 'https://api.papermc.io/v2/projects/paper/versions/1.19.4/builds/550/downloads/paper-1.19.4-550.jar',
                '1.16.5': 'https://api.papermc.io/v2/projects/paper/versions/1.16.5/builds/794/downloads/paper-1.16.5-794.jar',
                '1.12.2': 'https://api.papermc.io/v2/projects/paper/versions/1.12.2/builds/1620/downloads/paper-1.12.2-1620.jar',
                '1.8.8': 'https://api.papermc.io/v2/projects/paper/versions/1.8.8/builds/445/downloads/paper-1.8.8-445.jar'
            }, 'Purpur': {
                '1.20.1': 'https://api.purpurmc.org/v2/purpur/1.20.1/2050/download',
                '1.19.4': 'https://api.purpurmc.org/v2/purpur/1.19.4/1985/download',
                '1.18.2': 'https://api.purpurmc.org/v2/purpur/1.18.2/1632/download',
                '1.17.1': 'https://api.purpurmc.org/v2/purpur/1.17.1/1428/download',
                '1.16.5': 'https://api.purpurmc.org/v2/purpur/1.16.5/1171/download'
            }, 'Fabric': {
                '1.20.1': 'https://meta.fabricmc.net/v2/versions/loader/1.20.1/0.14.22/0.11.2/server/jar',
                '1.19.4': 'https://meta.fabricmc.net/v2/versions/loader/1.19.4/0.14.22/0.11.2/server/jar',
                '1.18.2': 'https://meta.fabricmc.net/v2/versions/loader/1.18.2/0.14.22/0.11.2/server/jar',
                '1.16.5': 'https://meta.fabricmc.net/v2/versions/loader/1.16.5/0.14.22/0.11.2/server/jar',
                '1.14.4': 'https://meta.fabricmc.net/v2/versions/loader/1.14.4/0.14.22/0.11.2/server/jar'            
            }
        }

        loop = True
        while loop:
            current = self.menu['Main'].display()
            if current == 'Servers':
                current = self.menu['Servers'].display()
                if current in self.getServers():
                    while True:
                        server = current
                        current = core.service.Menu(
                            self.piCraftText() + '\n' + current,
                            ['Start server', 'Delete']
                        ).display()

                        if current == 'Start server':
                            subprocess.run('start.bat', shell=True)
                            exit()
                        elif current == 'Delete':
                            current = self.menu['Confirm'].display()
                            if current == 'I am sure':
                                shutil.rmtree(server)
                                exit()


    def getServers(self):
        with open('store.json', 'r') as f:
            return json.load(f)['servers']

    def unpackJava(self):
        with tarfile.open('java.tar.gz', 'r:gz') as f:
            for member in f.getmembers():
                if member.name == 'jdk-17.0.8.1+1-jre/bin/java':
                    f.extract(member)
                    f.close()
                    
                    os.remove('java.tar.gz')
                    shutil.move(member.name, 'server/java')
                    shutil.rmtree(member.name.split('/')[0])
    
    def download(url: str, fileName: str, progressBar: core.service.ProgressBar, divider: int):
        with open(str(pathlib.Path(__file__).parent.resolve().parent.resolve())+'/'+fileName, 'ab+') as f:
            download, i = requests.get(url, stream=True), progressBar.percentage
            for chunk in download.iter_content(round(int(download.headers['Content-Length'])/divider)):
                f.write(chunk)
                progressBar.draw(i)
                i += 1
                
    def piCraftText(self): return '''
        \x1b[31m██████╗ ██╗\x1b[38;5;208m ██████╗██████╗  █████╗ ███████╗████████╗\x1b[39m
        \x1b[31m██╔══██╗██║\x1b[38;5;208m██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝\x1b[39m
        \x1b[31m██████╔╝██║\x1b[38;5;208m██║     ██████╔╝███████║█████╗     ██║   \x1b[39m
        \x1b[31m██╔═══╝ ██║\x1b[38;5;208m██║     ██╔══██╗██╔══██║██╔══╝     ██║   \x1b[39m
        \x1b[31m██║     ██║\x1b[38;5;208m╚██████╗██║  ██║██║  ██║██║        ██║   \x1b[39m
        \x1b[31m╚═╝     ╚═╝\x1b[38;5;208m ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   \x1b[39m
        '''

if __name__ == '__main__': App()