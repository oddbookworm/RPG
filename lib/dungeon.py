from random import choice, seed, randint
import pygame as pg
try:
    from prng import prng
    from graph import Graph
    from worldSpace import WorldSpace
    from room import RoomType, Room
    from cell import Cell
except ModuleNotFoundError:
    from .prng import prng
    from .graph import Graph
    from .worldSpace import WorldSpace
    from .room import RoomType, Room
    from .cell import Cell

class Dungeon(WorldSpace):
    def __init__(self, size, num_rooms, tile_size, dungeon_seed = None,
                custom_allowed = False):
        super().__init__(size)
        self.num_rooms = num_rooms
        self.dungeon_seed = dungeon_seed
        self.custom = custom_allowed
        self.tile_size = tile_size
        
        # choose the room types, in order
    def generate_rooms(self):
        seed(self.dungeon_seed)
        possible_types = list(RoomType)
        possible_types.remove(RoomType.HALL)
        if not self.custom:
            possible_types.remove(RoomType.CUSTOM)
        self.room_types = [choice(possible_types) for _ in range(self.num_rooms)]
        self.room_seeds = prng(self.dungeon_seed, self.num_rooms)
        self.room_sizes = [(randint(3 * self.tile_size, 10 * self.tile_size),
                            randint(3 * self.tile_size, 10 * self.tile_size)) 
                            for _ in range(self.num_rooms)]
        self.room_positions = [(randint(3 * self.tile_size, 10 * self.tile_size),
                                randint(3 * self.tile_size, 10 * self.tile_size)) 
                                for _ in range(self.num_rooms)]
        self.rooms = []
        self.non_walkable = []

    def generate_room(self, room_number, floor_tex):
        room_type = self.room_types[room_number]
        room_size = self.room_sizes[room_number]
        room_seed = self.room_seeds[room_number]
        room_pos = self.room_positions[room_number]
        room = Room(room_type, room_size)
        room.create_room(floor_tex, self.tile_size, room_seed)
        self.rooms.append([room, room_pos])
    
    def generate_walls(self, wall_tex):
        for room in self.rooms:
            room[0].create_walls(wall_tex, self.tile_size)

        for room in self.rooms:
            offset = room[1]
            for cell in room[0].cells:
                if not cell.is_walkable:
                    surf = cell.surface
                    pos = (cell.pos[0] + offset[0], cell.pos[1] + offset[1])
                    size = cell.size
                    tex = cell.texture
                    temp_cell = Cell(surf, tex, size, pos, False)

                    self.non_walkable.add(temp_cell)

if __name__ == "__main__":
    screen = pg.display.set_mode((100, 100))
    dungeon = Dungeon((100, 100), 10, 32, 1)