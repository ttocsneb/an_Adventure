# import curses
# https://docs.python.org/3/howto/curses.html
import adventurelib
from adventurelib import say
import time
from . import commands
import random

def printSlow(value, *args, **kwargs):
    value = str(value)
    for char in value:
        print(char, end='', flush=True)
        time.sleep((random.random() * .3) ** 2)
    print('')

def bootstrap():
    num_chars = random.randint(50, 250)
    # num_chars= 20000

    printSlow("Last login: somedate.exe")
    for _ in range(3):
        print('.')
        time.sleep(.7)

    for _ in range(num_chars):
        print(chr(random.randint(0x20, 254)), end='', flush=True)
        time.sleep((random.random() * 0.2) ** 2)
    
    printSlow("Welcome to the terminal\n")
    printSlow("- on v178.4.0-starthread")
    printSlow("-> screenfetch\n")

    global callSign
    callSign = input("Enter your Call Sign.\n")
    
    printSlow("__Access__Granted__\n\n\n")


def start():
    bootstrap()
    adventurelib.start()
    # curses.wrapper(main)