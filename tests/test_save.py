import unittest
from an_adventure.bagsOfHolding import items, rooms
from os import path

files = path.join(path.dirname(__file__), 'files')


class TestSaves(unittest.TestCase):

    def test_items(self):
        try:
            item_conf = items.loadItems()
        except Exception as e:
            self.fail(f"Could not load items.json:\n{e}")
        self.assertTrue(isinstance(item_conf, items.ItemConfig))

        # Check bad config files

        self.assertRaises(RuntimeError, items.loadItems, path.join(files, "missing_items.json"))
        self.assertRaises(RuntimeError, items.loadItems, path.join(files, "bad_type_items.json"))
        try:
            items.loadItems(path.join(files, "missing_attr_items.json"))
        except Exception as e:
            self.fail(f"missing attributes should not fail:\n{e}")

    def test_rooms(self):
        try:
            room_conf = rooms.loadRooms()
        except Exception as e:
            self.fail(f"Could not load rooms.json:\n{e}")
        self.assertTrue(isinstance(room_conf, rooms.RoomConfig))

        self.assertRaises(RuntimeError, rooms.loadRooms, path.join(files, "bad_name_rooms.json"))
        self.assertRaises(RuntimeError, rooms.loadRooms, path.join(files, "bad_desc_rooms.json"))
