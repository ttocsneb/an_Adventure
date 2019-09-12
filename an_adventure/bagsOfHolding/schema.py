import os
import json

from marshmallow import Schema, fields, post_load, pre_dump
import adventurelib


class ItemConfig:
    def __init__(self, items: list):
        self.items = items

    def __repr__(self):
        return f"<ItemConfig(items={self.items})>"


"""
{
    "names": [
        "Main Name",
        "alias Name 1",
        "alias Name 2"
    ],
    "attrs": {
        "edible": true,
    }
}
"""
class ItemSchema(Schema):
    names = fields.List(fields.String())
    attrs = fields.Dict()

    @post_load
    def createItem(self, data):
        item = adventurelib.Item(*data['names'])
        for attr, value in data['attrs'].items():
            setattr(item, attr, value)
        return item


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
    items = fields.Nested(ItemSchema, many=True)

    @post_load
    def createItemConfig(self, data: dict):
        return ItemConfig(**data)


def loadItems() -> ItemConfig:
    from os.path import dirname as d

    schema = ItemConfigSchema()

    config_path = os.path.join(d(d(d(__file__))), "items.json")

    with open(config_path) as file:
        conf_obj = dict(
            items=json.load(file)
        )
        config = schema.load(conf_obj)
    if config.errors:
        err_msg = ''.join(f'{k}: {", ".join(i for i in v)}' for k, v in config.errors.items())
        raise RuntimeError(f"Couldn't parse items.json\n{err_msg}")
    return config.data
