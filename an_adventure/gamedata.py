from marshmallow import Schema, fields, post_load
from os import path
import json
import adventurelib
import time

from os.path import dirname as d
import os

from . import schemas, cipher

_game_data_file = path.join(d(d(__file__)), 'saves')
timeStamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(_game_data_file)))
if not path.isdir(_game_data_file):
    os.mkdir(_game_data_file)


class GameData:
    def __init__(self, player: schemas.objects.Player, rooms: list, callsign: str):
        self.player = player
        self.rooms = rooms
        self.callsign = callsign
    
    def save(self):
        saveGameData(self)


class GameDataSchema(Schema):
    current_room = fields.String() #TODO make current_room a room reference
    player = fields.Nested(schemas.PlayerSchema)
    rooms = fields.Nested(schemas.RoomSchema, many=True)
    callsign = fields.String()

    @post_load
    def createGameData(self, data):
        return GameData(**data)


def getErrorString(errors):
    return ''.join(f'{k}: {", ".join(i for i in v)}' for k, v in errors.items())


def loadGameData(callsign: str) -> GameData:
    name_cipher = cipher.Cipher(ord(callsign[-1]), cipher.cipher_file)
    
    try:
        with open(path.join(_game_data_file, name_cipher.encodeStr(callsign) + '.json')) as file:
            schema = GameDataSchema()
            file_json = json.load(file)
            file_json['callsign'] = callsign
            game_data = schema.load(file_json)
    except OSError:
        return None

    if game_data.errors:
        errs = getErrorString(game_data.errors)
        raise RuntimeError(f"Could not load gamedata:\n{errs}")

    return game_data.data


def saveGameData(gameData: GameData):
    name_cipher = cipher.Cipher(ord(gameData.callsign[-1]), cipher.cipher_file)
    schema = GameDataSchema()
    data_dict = schema.dump(gameData)
    del data_dict.data['callsign']


    if data_dict.errors:
        errs = getErrorString(data_dict.errors)
        raise RuntimeError(f"Could not save gamedata:\n{errs}")

    with open(path.join(_game_data_file, name_cipher.encodeStr(gameData.callsign) + '.json'), 'w') as file:
        json.dump(data_dict.data, file)
