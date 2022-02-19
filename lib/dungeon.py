from random import choice, seed
import pygame as pg
try:
    from prng import prng
    from graph import Graph
    from worldSpace import WorldSpace
    from room import RoomType
except ModuleNotFoundError:
    from .prng import prng
    from .graph import Graph
    from .worldSpace import WorldSpace
    from .room import RoomType

class Dungeon(WorldSpace):
    def __init__(self, size, num_rooms, dungeon_seed = None, custom_allowed = False):
        super().__init__(size)
        self.num_rooms = num_rooms
        self.dungeon_seed = dungeon_seed
        seed(self.dungeon_seed)
        
        # choose the room types, in order
        possible_types = list(RoomType)
        if not custom_allowed:
            possible_types.remove(RoomType.CUSTOM)
        self.room_types = [choice(possible_types) for _ in range(self.num_rooms)]
        self.room_seeds = prng(self.dungeon_seed, num_rooms)

if __name__ == "__main__":
    screen = pg.display.set_mode((100, 100))
    dungeon = Dungeon((100, 100), 10, 1)