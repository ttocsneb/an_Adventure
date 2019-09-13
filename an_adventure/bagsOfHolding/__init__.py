import adventurelib
from adventurelib import say, when, Bag, Item
import time
import random
from .. import commands
from pymaybe import maybe

from . import items

config = items.loadItems()

inventory = Bag()
testRoom = Bag(config.items)


@when ('eat ITEM')
def eat(item):
    obj = inventory.find(item)
    if not obj:
        print(f'You do not have a {item}.')
    elif maybe(obj).edible == True:
        inventory.take(item)
        print(f'You eat the {obj}.')
    else:
        try:
            print(obj.eat_fail)
        except AttributeError:
            print(f'You can\'t eat the {obj}')


@when('inventory')
def show_inventory():
    print('You have:')
    if not inventory:
        print('nothing')
        return
    for item in inventory:
        print(f'* {item}')


@when("take ITEM")
def take(item):
    obj = testRoom.take(item)
    if not obj:
        print(f'there is no {item} here')
    else:
        inventory.add(obj)
        print(f'You have taken a {obj}.')


@when('look at ITEM')
def look(item):
    obj = maybe(inventory.find(item))
    if obj.is_none():
        print(f"You do not have a {item}.")
    else:
        if obj.color.is_some():
            print(f"It's a sort of {obj.color}-ish colour")
        if obj.size.is_some():
            print(f"it's about {obj.size}")
        