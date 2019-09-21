import adventurelib
from marshmallow import ValidationError

def load_items(item_names: list):
    """
    Load the item strings into a list of item objects

    raises KeyError
    """
    from .. import globalvars
    def get_item(item_name):
        try:
            return next(i for i in globalvars.items if i.name == item_name)
        except StopIteration:
            raise KeyError(item_name)
    
    return [get_item(i) for i in item_names]


class Gamedata:
    def __init__(self, current_room):
        self.current_room = current_room

class Player(adventurelib.Bag):
    def __init__(self, items: list = None):
        if items is None:
            items = list()
        
        items = load_items(items)

        for item in items:
            self.add(item)


class Room(adventurelib.Room):

    def __init__(self, name: str, desc: str, items: list = None, attrs: dict = None, exits: dict = None, item_desc: dict = None):
        object.__setattr__(self, '_init', False)
        super().__init__(desc)
        self.name = name
        self.desc = desc

        items = items or list()
        items = load_items(items)
        self._items = adventurelib.Bag(items)
        self._attrs = attrs or dict()
        self._exits = exits or dict()
        self._item_desc = item_desc or dict()

        if attrs is not None:
            for attr, value in attrs.items():
                setattr(self, attr, value)

        self._init = True

    def _load_exits(self, rooms: list):
        def get_room(name):
            return next(r for r in rooms if r.name == name)
        
        for d, room in self._exits.items():
            if isinstance(room, str):
                try:
                    room = get_room(room)
                except StopIteration:
                    raise KeyError(f"Could not find the room '{room}'")
            if not isinstance(room, Room):
                raise TypeError(f"'{room}' is not a valid room object")
            setattr(self, d, room)

    @property
    def items(self):
        return self._items

    @property
    def attrs(self):
        return self._attrs
    
    @property
    def exits(self):
        exits = dict((d, getattr(self, d)) for d in self._directions if getattr(self, d))
        return exits
    
    @property
    def item_desc(self):
        return self._item_desc

    def __setattr__(self, attr, value):
        if self._init and not isinstance(value, adventurelib.Room):
            self._attrs[attr] = value
        super().__setattr__(attr, value)
    
    def __repr__(self):
        return f"<Room(name='{self.name}', exits={self.exits}, attrs={self.attrs}, items={self.items})>"
