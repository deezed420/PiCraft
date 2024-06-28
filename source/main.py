from core.progress import ProgressBar
from core.menu import Menu

from psutil import virtual_memory
from os import get_terminal_size
from os.path import exists
from requests import get
from time import sleep

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
RAM = round(virtual_memory()[3]/1000000000)
if virtual_memory()[3]/1000000000 < 2: print('Warning: Less than 2GB RAM! There is little support for this. Expect lag and crashes.')
else: print('\nSystem has '+str(RAM)+'GB of RAM.')

print('\nChecking')