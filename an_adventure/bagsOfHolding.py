import adventurelib
from adventurelib import say, when, Bag, Item
import time
import random
from . import commands

dick = Item('dick', 'moby huge')
dick.colour = 'black'
dick.size = '3 feet tall'
paste = Item('Toothpaste (colgate)', 'toothpaste')
paste.colour = 'nebula'

inventory = Bag()
testRoom = Bag([dick, paste])

@when ('eat ITEM')
def eat(item):
    obj = inventory.take(item)
    if not obj:
        print(f'You do not have a {item}.')
    else:
        print(f'You eat the {obj}.')

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
    obj = inventory.find(item)
    if not item:
        print(f"You do not have a {item}.")
    else:
        print(f"It's a sort of {obj.colour}-ish colour")
        print(f"And it's about {obj.size}")