import os
import json

from marshmallow import Schema, fields, post_load, pre_dump
import adventurelib

from .. import schemas


class ItemConfig:
    def __init__(self, items: list):
        self.items = items

    def __repr__(self):
        return f"<ItemConfig(items={self.items})>"


"""
[
    {
        "names": [
            "Item Name"
        ]
    },
    {
        "names": [
            "item name"
        ],
        "attrs": {
            "bar": "foo"
        }
    }
]
"""
class ItemConfigSchema(Schema):
    items = fields.Nested(schemas.ItemSchema, many=True)
    rooms = fields.Nested(schemas.RoomSchema, many=True)

    @post_load
    def createItemConfig(self, data: dict):
        return ItemConfig(**data)


def loadItems() -> ItemConfig:
    from os.path import dirname as d

    schema = ItemConfigSchema()

    config_path = os.path.join(d(__file__), "items.json")

    with open(config_path) as file:
        conf_obj = dict(
            items=json.load(file)
        )

    config = schema.load(conf_obj)
    if config.errors:
        err_msg = ''.join(f'{k}: {", ".join(i for i in v)}' for k, v in config.errors.items())
        raise RuntimeError(f"Couldn't parse items.json\n{err_msg}")
    return config.data
