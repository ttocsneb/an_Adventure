from marshmallow import fields, Schema, post_load
import adventurelib
from pymaybe import maybe

from . import objects
from .. import globalvars

class ItemSchema(Schema):
    names = fields.List(fields.String())
    attrs = fields.Dict()

    @post_load
    def createItem(self, data):
        item = adventurelib.Item(*data['names'])
        for attr, value in data['attrs'].items():
            setattr(item, attr, value)
        return item


class ItemReference(fields.Field):
    default_error_messages = dict(
        dne="Item '{}' does not exist.", badobj="Invalid item object."
    )

    def __init__(self, items: list, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._items = items
    
    def _serialize(self, value: adventurelib.Item, attr, obj, **kwargs):
        if hasattr(value, "name"):
            return str(value.name)
        name = maybe(value).get('name')
        if name is None:
            self.fail("badobj")
        return str(name)
    
    def _deserialize(self, value: str, attr, obj, **kwargs):
        def get_items():
            if callable(self._items):
                return self._items()
            return self._items
        item = next((v for v in get_items() if v.name == value), None)
        if item is None:
            self.fail("dne", name=value)
        return item


class PlayerSchema(Schema):

    items = fields.List(ItemReference(lambda: globalvars.items))

    @post_load
    def createPlayer(self, data):
        return objects.Player(**data)


class RoomSchema(Schema):
    
    items = fields.List(ItemReference(lambda: globalvars.items))

    @post_load
    def createRoom(self, data):
        return objects.Room(**data)