from marshmallow import Schema, fields, post_load
from os import path
import json
import adventurelib

from os.path import dirname as d

from .bagsOfHolding import schema

_game_data_file = path.join(d(d(__file__)), "data.json")


class Player(adventurelib.Bag):
    def __init__(self, items: list):
        for item in items:
            self.add(item)


class Room(adventurelib.Bag):
    def __init__(self, items: list):
        for item in items:
            self.add(item)


class GameData:
    def __init__(self, player: Player):
        self.player = player


class PlayerSchema(Schema):

    items = fields.Nested(schema.ItemSchema, many=True)

    @post_load
    def createPlayer(self, data):
        return Player(**data)


class RoomSchema(Schema):

    items = fields.Nested(schema.ItemSchema, many=True)

    @post_load
    def createRoom(self, data):
        return Room(**data)


class GameDataSchema(Schema):
    player = fields.Nested(PlayerSchema)
    rooms = fields.Nested(RoomSchema)

    @post_load
    def createGameData(self, data):
        return GameData(**data)


def getErrorString(errors):
    return ''.join(f'{k}: {", ".join(i for i in v)}' for k, v in errors.items())


def loadGameData():
    with open(_game_data_file) as file:
        schema = GameDataSchema()
        file_json = json.load(file)
        game_data = schema.load(file_json)
    
    if game_data.errors:
        errs = getErrorString(game_data.errors)
        raise RuntimeError(f"Could not load gamedata:\n{errs}")

    return game_data.data


def saveGameData(gameData: GameData):
    schema = GameDataSchema()
    data_dict = schema.dump(gameData)

    if data_dict.errors:
        errs = getErrorString(data_dict.errors)
        raise RuntimeError(f"Could not save gamedata:\n{errs}")
    
    with open(_game_data_file, 'w') as file:
        json.dump(data_dict.data, file)
