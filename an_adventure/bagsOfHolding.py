import adventurelib
from adventurelib import say, when, Bag
import time
import random
from . import commands


inventory = Bag()

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