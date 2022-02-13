from math import floor
import pygame as pg
try:
    from room import Room, RoomType
except ModuleNotFoundError:
    from .room import Room, RoomType

class WorldSpace:
    def __init__(self, size, tile_size = 32):
        self.size = size
        self.rooms = []
        self.image = pg.Surface(self.size, pg.SRCALPHA, 32).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()

    def create_room(self, pos, size, room_type, floor_texture, tile_size):
        room = Room(room_type, size)
        room.create_room(floor_texture, tile_size)
        self.rooms.append([room, pos])

    def draw(self, screen, space_pos = None):
        if space_pos == None:
            space_pos = (0, 0)
        self.rect.topleft = space_pos

        for pair in self.rooms:
            pos = pair[1]
            room = pair[0]

            room.draw(pos, self.image)
        screen.blit(self.image, self.rect)