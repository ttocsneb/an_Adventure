from .bagsOfHolding import items as itemConfig, rooms as roomConfig
from . import gamedata
import adventurelib

adventurelib.Room.add_direction('up', 'down')

# Create an empty gamedata object for pylinter
save_data = gamedata.GameData("")

items = itemConfig.loadItems().items

rooms = roomConfig.loadRooms().rooms
