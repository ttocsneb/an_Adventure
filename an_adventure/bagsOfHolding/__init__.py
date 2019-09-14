import adventurelib
from adventurelib import say, when, Bag, Item
import time
import random
from .. import commands
from pymaybe import maybe

from . import items
from .. import globalvars


@when ('eat ITEM')
def eat(item):
    obj = globalvars.save_data.player.find(item)
    if not obj:
        print(f'You do not have a {item}.')
    elif maybe(obj).edible == True:
        globalvars.save_data.player.take(item)
        print(f'You eat the {obj}.')
    else:
        try:
            print(obj.eat_fail)
        except AttributeError:
            print(f'You can\'t eat the {obj}')


@when('inventory')
def inventory():
    print('You have:')
    if not globalvars.save_data.player:
        print('nothing')
        return
    for item in globalvars.save_data.player:
        print(f'* {item}')


# @when("take ITEM")
# def take(item):
#     obj = testRoom.take(item)
#     if not obj:
#         print(f'there is no {item} here')
#     else:
#         globalvars.save_data.player.add(obj)
#         print(f'You have taken a {obj}.')


@when('look at ITEM')
def look(item):
    obj = maybe(globalvars.save_data.player.find(item))
    if obj.is_none():
        print(f"You do not have a {item}.")
    else:
        if obj.color.is_some():
            print(f"It's a sort of {obj.color}-ish colour")
        if obj.size.is_some():
            print(f"it's about {obj.size}")
        