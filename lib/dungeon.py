from prng import prng
from ... import graph
from pprint import PrettyPrinter
from worldSpace import WorldSpace

class Dungeon(WorldSpace):
    def __init__(self, width, height, num_rooms):
        super().__init__(width, height)
        self.num_rooms = num_rooms

    