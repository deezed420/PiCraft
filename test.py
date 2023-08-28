from msvcrt import getch
import sys

while True:
    key = getch()
    if key == b'\x03':
        print('CTRL C detected. Press again to terminate.')
        key = getch()
        if key == b'\x03': sys.exit()
    print(key)