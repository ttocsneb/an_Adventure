# import curses
# https://docs.python.org/3/howto/curses.html
import adventurelib
from adventurelib import say
import time
from . import commands, gamedata, schemas
import random
import re

def printSlow(value, *args, **kwargs):
    value = str(value)
    for char in value:
        print(char, end='', flush=True)
        time.sleep((random.random() * .3) ** 2)
    print('')

def bootstrap():
    num_chars = random.randint(50, 150)
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

    callsign_pattern = re.compile(r"[^a-z0-9_\- ]+")

    valid_name = False
    while not valid_name:
        callSign = input("Enter your Call Sign.\n").lower()

        if next(re.finditer(callsign_pattern, callSign), False):
            print("Invalid CallSign!")
            print("Try again\n")
            continue
        valid_name = True

        data = gamedata.loadGameData(callSign)
        if data is None:
            printSlow("Creating account.....")
            data = gamedata.GameData(schemas.objects.Player(list()), list(), callSign)
            gamedata.saveGameData(data)
    
    printSlow("__Access__Granted__\n\n\n")


def start():
    bootstrap()
    adventurelib.start()
    # curses.wrapper(main)