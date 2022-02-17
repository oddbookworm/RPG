from math import floor
import pygame as pg
try:
    from room import Room, RoomType
    from cell import Cell
except ModuleNotFoundError:
    from .room import Room, RoomType
    from .cell import Cell

class WorldSpace:
    def __init__(self, size, tile_size = 32):
        """
        size: tuple of pixel sizes for the whole space
        tile_size: integer size of the tiles
        """
        self.size = size
        self.rooms = []
        self.image = pg.Surface(self.size, pg.SRCALPHA, 32).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.tile_size = tile_size
        self.non_walkable = pg.sprite.Group()

    def create_room(self, pos, size, room_type, floor_texture, seed = None):
        """
        pos: tuple of pixels defining relative position to self.image
        size: tuple of pixels defining width/height of the room
        room_type: room.RoomType value defining what type of room it is
        floor_texture: path to texture
        seed: the seed to feed a random room
        """
        room = Room(room_type, size)
        room.create_room(floor_texture, self.tile_size, seed = seed)
        self.rooms.append([room, pos])
    
    def create_walls(self, wall_texture):
        for room in self.rooms:
            room[0].create_walls(wall_texture, self.tile_size)

        for room in self.rooms:
            for cell in room[0].cells:
                if not cell.is_walkable:
                    self.non_walkable.add(cell)

    def draw(self, screen, space_pos = (0, 0)):
        """
        screen: the pygame.Surface that is to be drawn to
        space_pos: the position of self.image relative to screen
        """
        self.rect.topleft = space_pos

        for pair in self.rooms:
            pos = pair[1]
            room = pair[0]
            room.draw(pos, self.image)

        screen.blit(self.image, self.rect)