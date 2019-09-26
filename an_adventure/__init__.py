# import curses
# https://docs.python.org/3/howto/curses.html
import os
from pymaybe import maybe
import colorama
from colorama import Fore
import adventurelib
from adventurelib import say, Room
import time
from . import commands, gamedata, schemas, globalvars
from .util import printSlow, printSlowColor
import random
import re

def _handle_command(cmd):
    """Handle a command typed by the user."""
    ws = cmd.lower().split()

    for pattern, func, kwargs in adventurelib._available_commands():
        args = kwargs.copy()
        matches = pattern.match(ws)
        if matches is not None:
            globalvars.save_data.turn_counter += 1
            args.update(matches)
            func(**args)
            update_status()
            break
    else:
        no_command_matches(cmd)
    print()
adventurelib._handle_command = _handle_command    

def update_status():
    if maybe(globalvars.save_data.current_room).breathable == 1:
        globalvars.save_data.oxygen -= 10
    elif maybe(globalvars.save_data.current_room).breathable == 2:
        globalvars.save_data.oxygen -= 30
    else:
        globalvars.save_data.oxygen = min(globalvars.save_data.oxygen + 10, 100)

    if globalvars.save_data.oxygen <= 0:
        #TODO Deathscreen
        print("Death")



def no_command_matches(command):
    print(random.choice([
        Fore.CYAN + 'Your command is unknown.' + Fore.RESET,
        Fore.CYAN + 'I am unsure what you are atempting to do.' + Fore.RESET,
        Fore.RED + "Perhaps rephrase that into something more intelligable." + Fore.RESET
    ]))
adventurelib.no_command_matches = no_command_matches

def prompt():
    return  f'{Fore.CYAN}StarThreadCMD>{Fore.RESET} '
adventurelib.prompt = prompt

def bootstrap(skipIntro=False):
    if os.name == "nt":
        os.system('cls')
    else: 
        os.system('clear') 

    if gamedata.file_count < 2 and not skipIntro: #TODO create cheat code save
        printSlow("""You awake, your head aching.\n Getting up, you take in an unfamiliar surrounding, 
        and a terminal clicks to life directly in front of you.\n
        Random characters crawl accross its screen as it struggles to make sense of itself. \n\n""", max=100, corrupt=True)
        input("(press enter)")
    if os.name == "nt":
        os.system('cls')
    else: 
        os.system('clear')    

    if not skipIntro:

        printSlow(f"Last login: {gamedata.timeStamp}", max=50)
        for _ in range(3):
            print('.')
            time.sleep(.7)

        printSlowColor("Welcome to the terminal\n- on",
                       Fore.CYAN, " v178.4.0.st\n",
                       Fore.LIGHTBLACK_EX, "->screenfetch\n", Fore.RESET, max=50)
        printSlowColor(Fore.CYAN, """               ||
               ||
          ||   ||  ||
          ||   |╚==||=======╗|         Terranc3@Terminal3
          ||       ||       ||         OS: """, Fore.RESET, """StarThread""", Fore.CYAN, """
          ||       ||       ||         Kernel: """, Fore.RESET, """x172_86 StarThread 178.4.0-1-ION""", Fore.CYAN, """
          |╚============ ■  ||         Downtime: """, Fore.RESET, """1h 47m""", Fore.CYAN, """
                   ||       ||         Packages: """, Fore.RESET, """553""", Fore.CYAN, """
                   |╚=======||         Shell: """, Fore.RESET, """bjh 9.3.7""", Fore.CYAN, """
                    ████████||         Resolution: """, Fore.RESET, """1920x1080""", Fore.CYAN, """ 
                    ████████|/         WM: """, Fore.RESET, """i6""", Fore.CYAN, """
          ||        ███████//          Authorization: """, Fore.RESET, """Active""", Fore.CYAN, """ 
   |╔=====╗|        ██████//           Power Supply: """, Fore.RESET, """Limited""", Fore.CYAN, """ 
   ||     ||  =====||████//            Diagnostics: """, Fore.RESET, """Functional""", Fore.CYAN, """ 
   ||     ||       ||███//             CPU: """, Fore.RESET, """Quantum Core i9 980 @ 16x 44.816GHz [0.0°K]""", Fore.CYAN, """
   ||     |╚====   ||██//              GPU: """, Fore.RESET, """NEC µPD7220""", Fore.CYAN, """
   ||              ||█//               RAM: """, Fore.RESET, """6.2 Exabytes""", Fore.CYAN, """
                   ||//
                   \\|/
                    V \n""", Fore.RESET, max=5)

    callsign_pattern = re.compile(r"[^a-z0-9_\- ]+")

    valid_name = False
    while not valid_name:
        callSign = input("Enter your Call Sign.\n").lower()

        if not callSign or next(re.finditer(callsign_pattern, callSign), False):
            printSlowColor(Fore.RED, "Invalid CallSign!\n", Fore.RESET)
            continue
        valid_name = True

        globalvars.save_data = gamedata.loadGameData(callSign)
        if globalvars.save_data is None:
            printSlow("Creating account.....", corrupt=True)
            globalvars.save_data = gamedata.GameData(callSign, rooms=globalvars.rooms)
            globalvars.save_data.current_room = "terminal room"
            globalvars.save_data.save()
    
    printSlow("__Access__Granted__\n\n\n", corrupt=True)

    if globalvars.save_data.turn_counter == 0 and not skipIntro:
        #tutorial()
        pass




def start(skipIntro=False):
    from .bagsOfHolding import items
    colorama.init()
    bootstrap(skipIntro)
    adventurelib.start(help=False)