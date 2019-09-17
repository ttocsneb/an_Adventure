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
        "exits": {
            "direction": "room"
        }
    }
]
"""
class RoomsConfigSchema(Schema):
    rooms = fields.Nested(schemas.RoomSchema, many=True)

    @post_load
    def createRoomConfig(self, data: dict):
        return RoomConfig(**data)


def loadRooms() -> RoomConfig:
    from os.path import dirname as d

    schema = RoomsConfigSchema()

    config_path = os.path.join(d(__file__), "rooms.json")

    with open(config_path) as file:
        conf_obj = dict(
            rooms=json.load(file)
        )

    config = schema.load(conf_obj)
    if config.errors:
        err_msg = ''.join(f'{k}: {", ".join(i for i in v)}' for k, v in config.errors.items())
        raise RuntimeError(f"Couldn't parse rooms.json\n{err_msg}")
    return config.data