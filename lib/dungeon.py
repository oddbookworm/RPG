from prng import prng
from graph import Graph
from worldSpace import WorldSpace
from pprint import PrettyPrinter

class Dungeon(WorldSpace):
    def __init__(self, width, height, num_rooms):
        super().__init__(width, height)
        self.num_rooms = num_rooms

    