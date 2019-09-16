import adventurelib

class Gamedata:
    def __init__(self, current_room):
        self.current_room = current_room

class Player(adventurelib.Bag):
    def __init__(self, items: list = None):
        if items is None:
            items = list()
        for item in items:
            self.add(item)


class Room(adventurelib.Bag):
    def __init__(self, items: list = None):
        if items is None:
            items = list()
        for item in items:
            self.add(item)
