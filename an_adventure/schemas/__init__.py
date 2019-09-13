from marshmallow import fields, Schema, post_load
import adventurelib
from . import objects

class ItemSchema(Schema):
    names = fields.List(fields.String())
    attrs = fields.Dict()

    @post_load
    def createItem(self, data):
        item = adventurelib.Item(*data['names'])
        for attr, value in data['attrs'].items():
            setattr(item, attr, value)
        return item


class PlayerSchema(Schema):

    items = fields.Nested(ItemSchema, many=True)

    @post_load
    def createPlayer(self, data):
        return objects.Player(**data)


class RoomSchema(Schema):

    items = fields.Nested(ItemSchema, many=True)

    @post_load
    def createRoom(self, data):
        return objects.Room(**data)