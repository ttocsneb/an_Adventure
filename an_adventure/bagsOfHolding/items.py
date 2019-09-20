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

    @post_load
    def createItemConfig(self, data: dict):
        return ItemConfig(**data)


def loadItems(config_path=None) -> ItemConfig:
    from os.path import dirname as d

    schema = ItemConfigSchema()

    if not config_path:
        config_path = os.path.join(d(__file__), "items.json")

    with open(config_path) as file:
        conf_obj = dict(
            items=json.load(file)
        )

    config = schema.load(conf_obj)
    if config.errors:
        err_msg = schemas.getErrorString(config.errors)
        raise RuntimeError(f"Couldn't parse items.json\n{err_msg}")
    return config.data
