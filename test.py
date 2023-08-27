import core.services, time

p=core.services.progress()

try:
    for i in range(100):
        time.sleep(.1)
        if i != 50: p.draw(i)
        else: p.halt() ; input('deez?\n> ')
except KeyboardInterrupt: print('\x1b[2J ')