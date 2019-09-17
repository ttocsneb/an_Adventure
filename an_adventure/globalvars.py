from .bagsOfHolding import items as itemConfig, rooms as roomConfig
from . import gamedata


# Create an empty gamedata object for pylinter
save_data = gamedata.GameData("")

items = itemConfig.loadItems().items

rooms = roomConfig.loadRooms().rooms
