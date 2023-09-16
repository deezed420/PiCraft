import core.service
import subprocess
import requests
import tarfile
import pathlib
import shutil
import re
import os

class App:
    def __init__(self):
        self.errcode = ''
        self.links = {
            'Java': 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jre_aarch64_linux_hotspot_17.0.8.1_1.tar.gz',
            'Spigot': {
                '1.20.1': 'https://download.getbukkit.org/spigot/spigot-1.20.1.jar',
                '1.19.4': 'https://download.getbukkit.org/spigot/spigot-1.19.4.jar',
                '1.16.5': 'https://cdn.getbukkit.org/spigot/spigot-1.16.5.jar',
                '1.12.2': 'https://cdn.getbukkit.org/spigot/spigot-1.12.2.jar',
                '1.8.8': 'https://cdn.getbukkit.org/spigot/spigot-1.8.8-R0.1-SNAPSHOT-latest.jar'
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
        
        while True:
            config = core.service.ConfigFile('store.json')
            servers = config.getServers()
            
            self.menu = {
                'Main': core.service.Menu(
                    self.PineCraftXText() + '\nMain menu',
                    ['Servers', 'Settings', 'Destroy']
                ),
                'Servers': core.service.Menu(
                    self.PineCraftXText() + '\nServers',
                    ['Create new']+list(servers.keys())
                ),
                'Install': {
                    'Select': core.service.Menu(
                        self.PineCraftXText() + '\nSelect jar type',
                        ['Spigot', 'Paper', 'Purpur', 'Fabric']
                    ), 'Spigot': core.service.Menu(
                        self.PineCraftXText() + '\nSelect version of server',
                        ['1.20.1', '1.19.4', '1.16.5', '1.12.2', '1.8.8']
                    ), 'Paper': core.service.Menu(
                        self.PineCraftXText() + '\nSelect version of server',
                        ['1.20.1', '1.19.4', '1.16.5', '1.12.2', '1.8.8']
                    ), 'Purpur': core.service.Menu(
                        self.PineCraftXText() + '\nSelect version of server',
                        ['1.20.1', '1.19.4', '1.18.2', '1.17.1', '1.16.5']
                    ), 'Fabric': core.service.Menu(
                        self.PineCraftXText() + '\nSelect version of server',
                        ['1.20.1', '1.19.4', '1.18.2', '1.16.5', '1.14.4']
                    )
                },
                'Confirm': core.service.Menu(
                    self.PineCraftXText() + '\nAre you sure?',
                    ['I am sure', 'Nevermind']
                )
            }

            while True:
                current = self.menu['Main'].display()
                if current == 'Servers':
                    current = self.menu['Servers'].display()
                    if current in servers:
                        
                        servers = config.getServers()
                        server = current
                        current = core.service.Menu(
                            self.PineCraftXText() + '\n' + current,
                            ['Start server', 'Delete']
                        ).display()

                        if current == 'Start server':
                            subprocess.run('./'+server+'/run.sh', shell=True)
                            exit()
                        elif current == 'Delete':
                            current = self.menu['Confirm'].display()
                            if current == 'I am sure':
                                config.delServer(server)
                                shutil.rmtree(server)
                                break
                    else:
                        while True:
                            core.service.clear()
                            print(self.PineCraftXText())
                            print(self.errcode)
                            name = input('\nEnter name of server:\n> ')
                            if name == '':
                                self.errcode = 'Name cannot be empty. Please enter valid name.'
                            else:
                                if not re.match(r'^[^<>:"//|?*]*$', name):
                                    self.errcode = 'Invalid characters in name. Please enter valid name.'
                                else:
                                    jar = self.menu['Install']['Select'].display()
                                    v = self.menu['Install'][jar].display()

                                    p = core.service.ProgressBar('Downloading')

                                    os.mkdir(name)

                                    p.print('Downloading Java')
                                    self.download(self.links['Java'], name+'\java.tar.gz', p, 50)
                                    p.print('Unpacking Java')
                                    self.unpackJava(name+'/java.tar.gz')
                                    p.print('Downloading '+jar+' '+v)
                                    self.download(self.links[jar][v], name+'\server.jar', p, 50)
                                    p.title = 'Finishing'
                                    p.print('Agreeing to EULA')
                                    with open(name+'\eula.txt', 'w') as f: f.write('eula=true')
                                    config.addServer(name, jar, v)
                                    core.service.clear()
                                    print('Successfully installed',jar,v,'!')
                                    exit()


    def unpackJava(self, fileName):
        with tarfile.open(fileName, 'r:gz') as f:
            for member in f.getmembers():
                if member.name == 'jdk-17.0.8.1+1-jre/bin/java':
                    f.extract(member)
                    f.close()
                    
                    os.remove(fileName)
                    shutil.move(member.name, os.path.dirname(fileName)+'/java')
                    shutil.rmtree(member.name.split('/')[0])
    
    def download(self, url: str, fileName: str, progressBar: core.service.ProgressBar, divider: int):
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        with open(fileName, 'ab+') as f:
            download, i = requests.get(url, stream=True), progressBar.percentage
            for chunk in download.iter_content(round(int(download.headers['Content-Length'])/divider)):
                f.write(chunk)
                progressBar.draw(i)
                i += 1
                
    def PineCraftXText(self): 
        columns, _ = os.get_terminal_size()
        
        if columns <= 94:
            return '''
            \x1b[31m██████╗ \x1b[38;5;208m ██████╗\x1b[31m██╗  ██╗
            \x1b[31m██╔══██╗\x1b[38;5;208m██╔════╝\x1b[31m╚██╗██╔╝
            \x1b[31m██████╔╝\x1b[38;5;208m██║     \x1b[31m ╚███╔╝ 
            \x1b[31m██╔═══╝ \x1b[38;5;208m██║     \x1b[31m ██╔██╗ 
            \x1b[31m██║     \x1b[38;5;208m╚██████╗\x1b[31m██╔╝ ██╗
            \x1b[31m╚═╝     \x1b[38;5;208m ╚═════╝\x1b[31m╚═╝  ╚═╝\x1b[39m
            '''
        else:
            return '''
            \x1b[31m██████╗ ██╗███╗   ██╗███████╗\x1b[38;5;208m ██████╗██████╗  █████╗ ███████╗████████╗    \x1b[31m██╗  ██╗
            \x1b[31m██╔══██╗██║████╗  ██║██╔════╝\x1b[38;5;208m██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝    \x1b[31m╚██╗██╔╝
            \x1b[31m██████╔╝██║██╔██╗ ██║█████╗  \x1b[38;5;208m██║     ██████╔╝███████║█████╗     ██║       \x1b[31m ╚███╔╝ 
            \x1b[31m██╔═══╝ ██║██║╚██╗██║██╔══╝  \x1b[38;5;208m██║     ██╔══██╗██╔══██║██╔══╝     ██║       \x1b[31m ██╔██╗ 
            \x1b[31m██║     ██║██║ ╚████║███████╗\x1b[38;5;208m╚██████╗██║  ██║██║  ██║██║        ██║       \x1b[31m██╔╝ ██╗
            \x1b[31m╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝\x1b[38;5;208m ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝       \x1b[31m╚═╝  ╚═╝\x1b[39m
            '''

if __name__ == '__main__': App()