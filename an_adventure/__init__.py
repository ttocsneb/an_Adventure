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
        Fore.CYAN + 'Your command is unknown.' + Fore.RESET,
        Fore.CYAN + 'I am unsure what you are atempting to do.' + Fore.RESET,
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
    num_chars = random.randint(250, 350)
    if os.name == "nt":
        os.system('cls')
    else: 
        os.system('clear') 

    if gamedata.file_count <= 1: #TODO create cheat code save
        print("""You awake, your head aching.\n Getting up, you take in an unfamiliar surrounding, 
        and a terminal clicks to life directly in front of you.\n
        Random characters crawl accross its screen as it struggles to make sense of itself. \n\n""")
        input("(press enter)")
    if os.name == "nt":
        os.system('cls')
    else: 
        os.system('clear')    

    if not skipIntro:

        printSlow(f"Last login: {gamedata.timeStamp}")
        for _ in range(3):
            print('.')
            time.sleep(.7)

        for _ in range(num_chars):
            print(chr(random.randint(0x20, 254)), end='', flush=True)
            time.sleep((random.random() * 0.2) ** 2)
        
        printSlow("Welcome to the terminal\n")
        print("- on" + Fore.CYAN + " v178.4.0-st" + Fore.RESET)
        print(Fore.LIGHTBLACK_EX + "->screenfetch\n" + Fore.RESET)
        print(Fore.CYAN + """               ||
               ||
          ||   ||  ||
          ||   |╚==||=======╗|         Terranc3@Terminal3
          ||       ||       ||         OS: """ + Fore.RESET + """StarThread"""+Fore.CYAN+"""
          ||       ||       ||         Kernel: """+Fore.RESET+"""x172_86 StarThread 178.4.0-1-ION"""+Fore.CYAN+"""
          |╚============ ■  ||         Downtime: """+Fore.RESET+"""1h 47m"""+Fore.CYAN+"""
                   ||       ||         Packages: """+Fore.RESET+"""553"""+Fore.CYAN+"""
                   |╚=======||         Shell: """+Fore.RESET+"""bjh 9.3.7"""+Fore.CYAN+"""
                    ████████||         Resolution: """+Fore.RESET+"""1920x1080"""+Fore.CYAN+""" 
                    ████████|/         WM: """+Fore.RESET+"""i6"""+Fore.CYAN+"""
          ||        ███████//          Authorization: """+Fore.RESET+"""Active"""+Fore.CYAN+""" 
   |╔=====╗|        ██████//           Power Supply: """+Fore.RESET+"""Limited"""+Fore.CYAN+""" 
   ||     ||  =====||████//            Diagnostics: """+Fore.RESET+"""Functional"""+Fore.CYAN+""" 
   ||     ||       ||███//             CPU: """+Fore.RESET+"""Quantum Core i9 980 @ 16x 44.816GHz [0.0°K]"""+Fore.CYAN+"""
   ||     |╚====   ||██//              GPU: """+Fore.RESET+"""NEC µPD7220"""+Fore.CYAN+"""
   ||              ||█//               RAM: """+Fore.RESET+"""6.2 Exabytes"""+Fore.CYAN+"""
                   ||//
                   \\|/
                    V \n""")

    callsign_pattern = re.compile(r"[^a-z0-9_\- ]+")

    valid_name = False
    while not valid_name:
        callSign = input("Enter your Call Sign.\n").lower()

        if not callSign or next(re.finditer(callsign_pattern, callSign), False):
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