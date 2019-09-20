from marshmallow import fields, Schema, post_load, pre_dump, post_dump, ValidationError
import adventurelib
from pymaybe import maybe

from . import objects


def getErrorString(errors):
    def to_str(obj):
        if isinstance(obj, dict):
            return ', '.join(f'{v}' for k, v in obj.items())
        return ', '.join(i for i in obj)
    return ''.join(f'{k}: {to_str(v)}' for k, v in errors.items())


class ItemSchema(Schema):
    names = fields.List(fields.String(), required=True)
    attrs = fields.Dict(missing=dict())

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

    def _serialize(self, value: adventurelib.Item, attr, obj, **kwargs):
        if hasattr(value, "name"):
            return str(value.name)
        name = maybe(value)['name']
        if name is None:
            self.fail("badobj")
        return str(name)

    def _deserialize(self, value: str, attr, obj, **kwargs):
        # def get_items():
        #     if callable(self._items):
        #         return self._items()
        #     return self._items
        # item = next((v for v in get_items() if v.name == value), None)
        # if item is None:
        #     self.fail("dne", name=value)
        return str(value)


class RoomReference(fields.Field):
    default_error_messages = dict(
        badobj="Invalid room object."
    )

    def _serialize(self, value: objects.Room, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if hasattr(value, "name"):
            return str(value.name)
        name = maybe(value)['name']

        if name is None:
            self.fail("badobj")
        return str(name)
    
    def _deserialize(self, value, attr, obj, **kwargs):
        return str(value)


class PlayerSchema(Schema):

    items = fields.List(ItemReference())

    @pre_dump
    def loadPlayer(self, data: objects.Player):
        return dict(items=list(data))

    @post_load
    def createPlayer(self, data):
        return objects.Player(**data)


class RoomSchema(Schema):
    
    name = fields.String(required=True)
    desc = fields.String(required=True)
    items = fields.List(ItemReference())
    attrs = fields.Dict()
    exits = fields.Dict()

    @post_dump
    def loadRoom(self, data: dict):
        def get_name(obj):
            if isinstance(obj, str):
                return obj
            if isinstance(obj, objects.Room):
                return obj.name
            raise ValidationError(f"type {type(obj)} is not a Room")
        data['exits'] = dict((k, get_name(v)) for k, v in data['exits'].items())
        return data

    @post_load
    def createRoom(self, data):
        return objects.Room(**data)
