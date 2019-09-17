# import curses
# https://docs.python.org/3/howto/curses.html
import os
import colorama
from colorama import Fore
import adventurelib
from adventurelib import say
import time
from . import commands, gamedata, schemas, globalvars
import random
import re

def no_command_matches(command):
    print(random.choice([
        'Your command is unknown.',
        'I am unsure what you are atempting to do.',
        Fore.RED + "Perhaps rephrase that into something more intelligable." + Fore.RESET
    ]))

adventurelib.no_command_matches = no_command_matches

def printSlow(value, *args, **kwargs):
    value = str(value)
    for char in value:
        print(char, end='', flush=True)
        time.sleep((random.random() * .3) ** 2)
    print('')

def bootstrap(skipIntro=False):
    num_chars = random.randint(50, 150)
    # num_chars= 20000

    if not skipIntro:

        printSlow(f"Last login: {gamedata.timeStamp}")
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

        globalvars.save_data = gamedata.loadGameData(callSign)
        if globalvars.save_data is None:
            printSlow("Creating account.....")
            globalvars.save_data = gamedata.GameData(callSign, rooms=globalvars.rooms)
            globalvars.save_data.current_room = "terminal"
            globalvars.save_data.save()
    
    printSlow("__Access__Granted__\n\n\n")


def start(skipIntro=False):
    from .bagsOfHolding import items
    colorama.init()
    bootstrap(skipIntro)
    adventurelib.start()
