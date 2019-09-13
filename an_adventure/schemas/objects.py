import adventurelib


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
