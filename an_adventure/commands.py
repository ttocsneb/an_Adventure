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

@when ('put ITEM')
def put(item):
    obj = globalvars.save_data.player.find(item)
    if not obj:
        print(f'You do not have a {item}.')
    elif maybe(obj).put_in.is_some() and globalvars.save_data.current_room.name in obj.put_in: 
        respond(obj, 'room_put_succ', f'You place the {obj} in the {globalvars.save_data.current_room}')
        globalvars.save_data.player.take(obj)
        globalvars.save_data.current_room.add(obj)
    else:
        respond(obj, 'room_put_fail', f'You cannot put a {obj} here.')    

@when ('put ITEM on TARGET')
def puton(item, target):
    obj = globalvars.save_data.player.find(item)
    tarobj = globalvars.save_data.current_room.find(target)
    if not obj: 
        print(f'You do not have a {item}.')
    elif not tarobj:
        print(f'There is no {target} to put the {obj} on')
    elif maybe(obj).put_on.is_some and tarobj.name in obj.put_on:
        respond(obj, f'put_succ_{target}', f'You put the {obj} on the {tarobj}')
        globalvars.save_data.player.take(obj)
        #TODO make it so that the item actualy gets put on the target
    else:
        respond(obj, f'put_fail_{tarobj}', f'You can\'t put the {obj} on the {tarobj}')    


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

@when('enter NEWROOM')
def go(newroom):
    direction = next((k for k, v in globalvars.save_data.current_room.exits.items() if v.name.startswith(newroom.replace('the ', ''))), None)
    if direction is None:
        print(f"You can't go there, {newroom} isn't a room")
        return
    room = globalvars.save_data.current_room.exit(direction)
    if room:
        globalvars.save_data.current_room = room
        print(f'You go to the {room.name}')
        look()
    else:
        print("Looks like that's not a valid option at the momment.")    

@when('save')
def save():
    globalvars.save_data.save()
    print(Fore.CYAN + 'I have saved your progress' + Fore.RESET)


@when('look')
def look():
    print(f'{globalvars.save_data.current_room.desc}\n')
    if globalvars.save_data.current_room.items:
        print("Inside, there is")
        for item in globalvars.save_data.current_room.items:
            print(f'- a {item}')
        print('')
    
    if globalvars.save_data.current_room.exits:
        print("From here you can go to")
        for room in globalvars.save_data.current_room.exits.values():
            print(f"- the {room.name}")
