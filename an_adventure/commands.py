import adventurelib
import colorama
from colorama import Fore
from adventurelib import say, when, Bag, Item
import time
import random
from pymaybe import maybe
from . import globalvars


def respond(obj, attr, default):
    if hasattr(obj, attr):
        print(getattr(obj, attr))
    else:
        print(default)


@when ('eat ITEM')
def eat(item):
    obj = globalvars.save_data.player.find(item)
    if not obj:
        print(f'You do not have a {item}.')
    elif maybe(obj).edible == True:
        globalvars.save_data.player.take(item)
        respond(obj, 'eat_succ', f'You eat the {obj}.')
    else:
        respond(obj, 'eat_fail', f'You can\'t eat the {obj}.')
        


@when('inventory')
def inventory():
    print('You have:')
    if not globalvars.save_data.player:
        print('nothing')
        return
    for item in globalvars.save_data.player:
        print(f'* {item}')


@when("take ITEM")
def take(item):
    obj = globalvars.save_data.current_room.items.take(item)
    if not obj:
        print(f'there is no {item} here')
    elif maybe(obj).immovable == True:
        globalvars.save_data.current_room.items.add(obj)
        respond(obj, 'take_fail', f'You cannot take the {obj}.')
    else:    
        globalvars.save_data.player.add(obj)
        respond(obj, 'take_succ', f'You have taken a {obj}.')


@when('look at ITEM')
def lookat(item):
    obj = maybe(globalvars.save_data.player.find(item))
    if obj.is_none():
        print(f"You do not have a {item}.")
    else:
        if obj.color.is_some():
            print(f"It's a sort of {obj.color}-ish colour")
        if obj.size.is_some():
            print(f"it's about {obj.size}")


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