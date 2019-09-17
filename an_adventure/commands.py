import adventurelib
import colorama
from colorama import Fore
from adventurelib import say, when, Bag, Item
import time
import random
from . import globalvars


@when("brush teeth")
def brush_teeth():
    obj = globalvars.save_data.player.find('toothpaste')
    if not obj:
        print('you have no toothpaste')
    else:
        say(""" 
            You squirt a bit too much toothpaste onto your
            brush and dozily jiggle it round your mouth.

            Your teeth feel clean and shiny now, as you
            run your tongue over them.
        """)

@when('exit DIRECTION')
def go(direction):
    room = globalvars.save_data.current_room.exit(direction)
    if room:
        globalvars.save_data.current_room = room
        print(f'You go {direction}')
        look()

@when('save')
def save():
    globalvars.save_data.save()
    print(Fore.CYAN + 'I have saved your progress' + Fore.RESET)


@when('look')
def look():
    print(globalvars.save_data.current_room.desc)