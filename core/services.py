import sys, os

CODE_SAVE_CURSOR = "\033[s"
CODE_RESTORE_CURSOR = "\033[u"
CODE_CURSOR_IN_SCROLL_AREA = "\033[1A"
COLOR_FG = '\033[30m'
COLOR_BG = '\033[42m'
COLOR_BG_BLOCKED = '\033[43m'
RESTORE_FG = '\033[39m'
RESTORE_BG = '\033[49m'

PROGRESS_BLOCKED = False
CURRENT_NR_LINES = 0
START_TIME = 0
RATE_BAR = True

class progress:
    def __init__(self) -> None:
        _, lines = os.get_terminal_size()

        print('\x1b[2J', end='')
        print("\n", end='')
        print(CODE_SAVE_CURSOR, end='')
        print("\033[0;" + str(lines) + "r", end='')
        print(CODE_RESTORE_CURSOR)
        print(CODE_CURSOR_IN_SCROLL_AREA, end='')

        self.draw(0)
    
    def draw(self, percentage: int):
        global PROGRESS_BLOCKED
        if PROGRESS_BLOCKED: PROGRESS_BLOCKED = False
        _, lines = os.get_terminal_size()
        self.percentage = percentage

        print(CODE_SAVE_CURSOR, end='')
        print("\033[" + str(lines) + ";0f", end='')

        print('\r', flush=True, end='')

        self.__print_bar_text(percentage)
        print(CODE_RESTORE_CURSOR, end='')

    def halt(self):
        _, lines = os.get_terminal_size()
        global PROGRESS_BLOCKED
        PROGRESS_BLOCKED = True
        print(CODE_SAVE_CURSOR, end='')
        print("\033[" + str(lines) + ";0f", end='')

        print('\r', flush=True, end='')

        self.__print_bar_text(self.percentage)
        print('\x1b[H', flush=True, end='')
        print()
    print(CODE_RESTORE_CURSOR, end='')
    def destroy(self):
        print('\x1b[2J]', end='')

    def __print_bar_text(self, percentage: str):
        
        color = f"{COLOR_FG}{COLOR_BG}"
        if PROGRESS_BLOCKED:
            color = f"{COLOR_FG}{COLOR_BG_BLOCKED}"

        cols, _ = os.get_terminal_size()
        r_bar = ""
        bar_size = cols - 17

        complete_size = (bar_size * percentage) / 100
        remainder_size = bar_size - complete_size

        progress_bar = f"[{color}{'#' * int(complete_size)}{RESTORE_FG}{RESTORE_BG}{'.' * int(remainder_size)}]"
        print(f" Progress {percentage}% {progress_bar} {r_bar}\r", end='')