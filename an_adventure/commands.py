import adventurelib
import colorama
from colorama import Fore
from adventurelib import say, when, Bag, Item
import time
import random
import os
from pymaybe import maybe
from . import globalvars
from . import gamedata
from .util import printSlow, printSlowColor


def Death(condition, custom):
    if custom:
        print(custom)
    elif condition == "starve":
        print("You feel starvation drag your mind into delerium.")      
    elif condition == "thirst":
        print("Your throat as dry as the desert, you slip into unconsiousness.")
    elif condition == "suffocate":
        print("You claw at your throat and try to draw in one last breath, but you fade into the black.")
    elif condition == "wounds":
        print("Body aching and blood pooling, you sucumb to your wounds.")
    
    if os.name == "nt":
        os.system('cls')
    else: 
        os.system('clear') 

    globalvars.save_data = gamedata.loadGameData(globalvars.save_data.callsign)              

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
        respond(obj, f'{globalvars.save_data.current_room.name}_put_succ', f'You place the {obj} in the {globalvars.save_data.current_room.name}')
        globalvars.save_data.player.take(item)
        globalvars.save_data.current_room.items.add(obj)
    else:
        respond(obj, 'room_put_fail', f'You cannot put a {obj} here.')    

@when ('put ITEM on TARGET')
def puton(item, target):
    obj = globalvars.save_data.player.find(item)
    tarobj = globalvars.save_data.current_room.items.find(target)
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

@when ('use ITEM')
def use(item):
    obj = globalvars.save_data.player.find(item)
    if not obj:
        print(f'You do not have a {item}.')
    elif maybe(obj).use == True: 
        respond(obj, 'use_succ', f'You use the {obj}.')
        if maybe(obj).single_use == True:
            globalvars.save_data.player.take(item)
    else:
        respond(obj, 'use_fail', f'You cannot use a {obj} now.') 

@when ('use ITEM on TARGET')
def useon(item, target):
    obj = globalvars.save_data.player.find(item)
    tarobj = globalvars.save_data.current_room.items.find(target)
    if not obj: 
        print(f'You do not have a {item}.')
    elif tarobj.is_none:
        print(f'There is no {target} to use the {obj} on')
    elif maybe(obj).use_on.is_some and tarobj.name in obj.use_on:
        respond(obj, f'use_succ_{target}', f'You use the {obj} on the {tarobj}')
        if maybe(obj).single_use == True:
            globalvars.save_data.player.take(item)
        #TODO make it so that the item actualy gets used on the target
    else:
        respond(obj, f'use_fail_{tarobj}', f'You can\'t use the {obj} on the {tarobj}')

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
        print(f'-a {item}')


@when("take ITEM")
def take(item):
    obj = globalvars.save_data.current_room.items.find(item)
    if not obj:
        print(f'there is no {item} here')
    elif maybe(obj).immovable == True:
        respond(obj, 'take_fail', f'You cannot take the {obj}.')
    else:    
        globalvars.save_data.current_room.items.take(item)
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
    obj = maybe(globalvars.save_data.player.find('toothpaste'))
    if obj.is_none:
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
        print(f"You can't go there, {newroom} isn't a room you can reach from here")
        return
    room = globalvars.save_data.current_room.exit(direction)
    if room:
        globalvars.save_data.current_room = room
        print(f'You go to the {room.name}')
        look()
        update_status()

def update_status():
    globalvars.save_data.nutrition -= 1
    globalvars.save_data.hydration -= 1
    if maybe(globalvars.save_data).nutrition == 1:
        printSlowColor(Fore.RED + "Blood sugar levels are dangerously low." + Fore.RESET)
    if maybe(globalvars.save_data).hyrdration == 1:
        printSlowColor(Fore.RED + "H2O content of blood is dangerously low." + Fore.RESET)
    if globalvars.save_data.nutrition < 1:
        Death("starve", None)
    elif globalvars.save_data.hydration < 1:
        Death("thirst", None)

@when('save')
def save():
    globalvars.save_data.save()
    print(Fore.CYAN + 'I have saved your progress' + Fore.RESET)


@when('look')
def look():
    print(f'{globalvars.save_data.current_room.desc}\n')
    if globalvars.save_data.current_room.items:
        print("Inside, there is:")
        for item in globalvars.save_data.current_room.items:
            print(f'- a {item}')
        print('')
    
    if globalvars.save_data.current_room.exits:
        print("From here you can go to:")
        for room in globalvars.save_data.current_room.exits.values():
            print(f"- the {room.name}")
        print('')    

    if maybe(globalvars.save_data.current_room).breathable == 1:
        respond(globalvars.save_data.current_room, 'O2_depleted_message', "Your environment is depleted of oxygen.")
        print('')   
    elif maybe(globalvars.save_data.current_room).breathable == 2:
        respond(globalvars.save_data.current_room, 'vacuum_message', "Your environment is exposed to the vacuum of space.")
        print('')   

     