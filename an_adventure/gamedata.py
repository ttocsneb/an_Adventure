from marshmallow import Schema, fields, post_load, ValidationError
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
    def __init__(self, callsign: str, player: schemas.objects.Player = None, rooms: list = None, current_room: str = None):
        self.callsign = callsign
        self.player = player or schemas.objects.Player()
        self.rooms = rooms or list()

        for room in self.rooms:
            room._load_exits(self.rooms)

        if current_room is not None:
            self.current_room = current_room
        else:
            self._current_room = None
    
    @property
    def current_room(self):
        return self._current_room
    
    @current_room.setter
    def current_room(self, value):
        if isinstance(value, schemas.objects.Room):
            self._current_room = value
            return
        if isinstance(value, str):
            room = self.getRoom(value)
            if room is not None:
                self._current_room = room
                return
            print(self.rooms)
        raise KeyError(f"Could not find the room '{value}'")

    def getRoom(self, name, default=None):
        try:
            return next(r for r in self.rooms if r.name == name)
        except StopIteration:
            pass
        return default

    def save(self):
        saveGameData(self)


class GameDataSchema(Schema):
    current_room = schemas.RoomReference()
    player = fields.Nested(schemas.PlayerSchema)
    rooms = fields.Nested(schemas.RoomSchema, many=True)
    callsign = fields.String()

    @post_load
    def createGameData(self, data):
        return GameData(**data)


def getErrorString(errors):
    def to_str(obj):
        if isinstance(obj, dict):
            return ', '.join(f'{v}' for k, v in obj.items())
        return ', '.join(i for i in obj)
    return ''.join(f'{k}: {to_str(v)}' for k, v in errors.items())


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
        print(game_data.errors)
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
