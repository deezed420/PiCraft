import sys

class Menu:
    def __init__(self, title: str, options: list):
        print('\x1b[2J', end='\r')

    def __getkey(self):
        firstChar = self.__getch()
        if sys.platform == 'linux':
            if firstChar == '\x1b':
                return {'[A': 'up', '[B': 'down', '[C': 'right', '[D': 'left'}[self.__getch() + self.__getch()]
            else: return firstChar
        else:
            if firstChar == b'\xe0':
                return {'H': 'up', 'P': 'down', 'M': 'right', 'K': 'left'}[self.__getch()]
            elif firstChar == b'\x03': raise KeyboardInterrupt
            else: return firstChar

    def __getch():
        if sys.platform == 'linux':
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch
        elif sys.platform == 'win32': from msvcrt import getch ; return getch

if __name__ == '__main__': Menu('e', [])