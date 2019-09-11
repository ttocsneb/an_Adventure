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
    num_chars = random.randint(10, 500)
    # num_chars= 2000

    for _ in range(num_chars):
        print(chr(random.randint(0, 255)), end='', flush=True)
        time.sleep((random.random() * 0.3) ** 2)
    printSlow("Welcome to the terminal")
    printSlow("Last login: somedate.exe\n")
    printSlow("Enter the passphrase.")


def start():
    bootstrap()
    adventurelib.start()
    # curses.wrapper(main)
