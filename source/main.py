from core.progress import ProgressBar
from core.menu import Menu

from psutil import virtual_memory, disk_usage, getloadavg
from os import get_terminal_size
from requests import get
from time import sleep
import pathlib

if get_terminal_size()[0] < 85: print("""
    ██████╗  ██████╗██╗  ██╗
    ██╔══██╗██╔════╝╚██╗██╔╝
    ██████╔╝██║      ╚███╔╝ 
    ██╔═══╝ ██║      ██╔██╗ 
    ██║     ╚██████╗██╔╝ ██╗
    ╚═╝      ╚═════╝╚═╝  ╚═╝""")

else: print("""
\x1b[38;5;196m██████╗ ██╗███╗   ██╗███████╗ ██████╗██████╗  █████╗ ███████╗████████╗\x1b[38;5;82m    ██╗  ██╗
\x1b[38;5;196m██╔══██╗██║████╗  ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝\x1b[38;5;82m    ╚██╗██╔╝
\x1b[38;5;196m██████╔╝██║██╔██╗ ██║█████╗  ██║     ██████╔╝███████║█████╗     ██║   \x1b[38;5;82m     ╚███╔╝ 
\x1b[38;5;196m██╔═══╝ ██║██║╚██╗██║██╔══╝  ██║     ██╔══██╗██╔══██║██╔══╝     ██║   \x1b[38;5;82m     ██╔██╗ 
\x1b[38;5;196m██║     ██║██║ ╚████║███████╗╚██████╗██║  ██║██║  ██║██║        ██║   \x1b[38;5;82m    ██╔╝ ██╗
\x1b[38;5;196m╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   \x1b[38;5;82m    ╚═╝  ╚═╝\x1b[0m""")

if get_terminal_size()[1] < 10: print('This terminal is too small!') ; exit()

print('\n\nChecking system...')
sleep(.5)

RAM = round(virtual_memory()[3]/1000000000)
if virtual_memory()[3]/1000000000 < 2: print('Warning: Less than 2GB RAM! Expect lag and crashes.')
else: print('\nSystem has '+str(RAM)+'GB of RAM.')

print('\nChecking files...')
sleep(.2)
scriptdir = str(pathlib.Path(__file__).parent)
pathlib.Path(scriptdir+'/data').mkdir(parents=True, exist_ok=True)
pathlib.Path(scriptdir+'/servers').mkdir(parents=True, exist_ok=True)

print('\nLoading servers...')
sleep(.5)

servers = {}
for path in pathlib.Path(scriptdir+'/servers').iterdir():
    if path.is_dir():
        for file in path.iterdir(): 
            if file.is_file() and file.name == 'config.bbcf':
                servers[path.name] = dict(line.strip().split('=') for line in file.read_text().split())
                

print(servers)