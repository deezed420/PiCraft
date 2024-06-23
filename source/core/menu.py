from sys import stdin,platform,stdout
from os import get_terminal_size

class Menu:
    def __init__(self, title: str, options: list) -> str:
        self.title = title
        self.options = options
        self._selected_index = 0
    
    def display(self, selector: str = '>', backSignal: bool = True, helpBar: bool = True):
        self.selector = selector
        
        _,rows = get_terminal_size()

        print('\x1b[2J')
        if helpBar:
            if backSignal: print(f'\x1b[{rows};0f Left - Back, Up and down - Move up and down, Enter - Select\r')
            else: print(f'\x1b[{rows};0f Left - Back, Up and down - Move up and down, Enter - Select \r')

        while True:
            self.__display_menu()
            key = self.__getkey()

            if key == 'up' and self._selected_index > 0: self._selected_index -= 1
            if key == 'down' and self._selected_index < len(self.options) - 1: self._selected_index += 1
            if key == 'select':  print('\x1b[2J') ; return self.options[self._selected_index]
            if backSignal and key == 'left': return 'Back'

    def __getch(self):
        if platform == 'linux':
            import termios, tty
            fd = stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch
        elif platform == 'win32':
            from msvcrt import getch
            return getch()

    def __getkey(self):
        firstChar = self.__getch()
        try:
            if platform == 'linux':
                if firstChar == '\x1b':
                    return {'[A': 'up', '[B': 'down', '[C': 'right', '[D': 'left'}[self.__getch() + self.__getch()]
                elif firstChar == chr(3):
                    raise KeyboardInterrupt
                elif firstChar in [chr(10), chr(13)]:
                    return 'select'
                else:
                    return firstChar
            else:
                if firstChar == b'\xe0':
                    return {'H': 'up', 'P': 'down', 'M': 'right', 'K': 'left'}[self.__getch().decode()]
                elif firstChar == b'\x03':
                    raise KeyboardInterrupt
                elif firstChar == b'\r':
                    return 'select'
                else:
                    return firstChar
        except KeyError: pass
            
    def __display_menu(self):
        stdout.write('\033[H')
        stdout.flush()

        print(self.title)

        for idx, option in enumerate(self.options):
            if idx == self._selected_index:
                print(f"{self.selector} {option}")
            else:
                print(f"  {option}")

if __name__ == '__main__': menu = print(Menu('Main Menu', ['Option 1', 'Option 2', 'Option 3']).display())