try:
    from prng import prng
    from graph import Graph
    from worldSpace import WorldSpace
except ModuleNotFoundError:
    from .prng import prng
    from .graph import Graph
    from .worldSpace import WorldSpace

class Dungeon(WorldSpace):
    def __init__(self, size, num_rooms):
        super().__init__(size)
        self.num_rooms = num_rooms

    