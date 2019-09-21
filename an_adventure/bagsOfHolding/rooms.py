import os
import json

from marshmallow import Schema, fields, post_load, pre_dump
import adventurelib

from .. import schemas

class RoomConfig:
    def __init__(self, rooms: list):
        self.rooms = rooms
    def __repr__(self):
        return f"<RoomConfig(rooms={self.rooms})>"


"""
[
    {
        "name": "room name",
        "desc": "room description",
        "attrs": {
            "bar": "foo"
        },
        "items": [
            "item name"
        ],
        "item_desc": {
            "item": "desc"
        }
        "exits": {
            "direction": "room"
        }
    }
]
"""
#TODO add item_desc so I can succ them into the look() command
class RoomsConfigSchema(Schema):
    rooms = fields.Nested(schemas.RoomSchema, many=True)

    @post_load
    def createRoomConfig(self, data: dict):
        rooms = data['rooms']
        for room in rooms:
            room._load_exits(rooms)
        return RoomConfig(**data)


def loadRooms(config_path=None) -> RoomConfig:
    from os.path import dirname as d

    schema = RoomsConfigSchema()

    if not config_path:
        config_path = os.path.join(d(__file__), "rooms.json")

    with open(config_path) as file:
        conf_obj = dict(
            rooms=json.load(file)
        )

    config = schema.load(conf_obj)
    if config.errors:
        err_msg = schemas.getErrorString(config.errors)
        raise RuntimeError(f"Couldn't parse rooms.json\n{err_msg}")
    return config.data