from enum import Enum, auto
import pygame as pg
try:
    from map_handler import loader
except ModuleNotFoundError:
    from .map_handler import loader
from pathlib import Path
import logging
try:
    from cell import Cell
    from config import SETTINGS
except ModuleNotFoundError:
    from .cell import Cell
    from .config import SETTINGS

class AutoName(Enum):
    """Meant to be subclassed
    Subclasses assign names instead of ints when auto() is used
    """
    def _generate_next_value_(name, start, count, last_values):
        return name

class RoomType(AutoName):
    """The types that rooms can have"""
    RANDOM = auto()
    RECTANGLE = auto()
    ROUND = auto()
    HALLWAY = auto()
    CUSTOM = auto()

class Room:
    def __init__(self, room_type: RoomType, size: tuple[int], pos: tuple[int] = (0, 0)):
        """room_type: one of the values from the RoomType Enum
        size: tuple of pixels (width, height)
        pos: tuple of pixels (x, y) offset from the Surface being drawn onto
        """
        self.room_type = room_type
        self.size = size
        self.pos = pos
        self.cells = []
        self.create_surface()

    def create_surface(self):
        self.image = pg.Surface(self.size, pg.SRCALPHA, 32).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
    
    def resize_surface(self):
        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        for cell in self.cells:
            cell.swap_world(self.image)

    def create_room(self, seed):
        """floor_texture: path to a texture
        tile_size: int of tile size
        seed: used to generate a random room
        """
        self.seed = seed
        if self.room_type == RoomType.RECTANGLE:
            self.generate_rect_room()
        
        if self.room_type == RoomType.ROUND:
            self.generate_round_room()

        if self.room_type == RoomType.RANDOM:
            self.generate_random_room()

    def draw(self, screen):
        for cell in self.cells:
            cell.draw()
        screen.blit(self.image, self.rect)
        
    def generate_rect_room(self):
        tile_size = SETTINGS['GENERAL']['TILESIZE']
        width_tiles = self.size[0] // tile_size
        height_tiles = self.size[1] // tile_size
        room_dir = ''.join([str(Path(__file__).parent.parent),
                            "\\assets\\rooms\\rect_rooms\\"])
        room = ''.join([room_dir, f'{width_tiles}x{height_tiles}_rect.json'])
        logging.info(f'Loaded {room} at position {self.pos}')
        data = loader.load_map(room)
        self.cells = loader.extract_cells(data, self.image)
        self.size = (data['Width'], data['Height'])
        self.resize_surface()

    def generate_round_room(self):
        tile_size = SETTINGS['GENERAL']['TILESIZE']
        width_tiles = self.size[0] // tile_size
        height_tiles = self.size[1] // tile_size
        room_dir = ''.join([str(Path(__file__).parent.parent),
                            "\\assets\\rooms\\ell_rooms\\"])
        room = ''.join([room_dir, f'{width_tiles}x{height_tiles}_ell.json'])
        logging.info(f'Loaded {room} at position {self.pos}')
        data = loader.load_map(room)
        self.cells = loader.extract_cells(data, self.image)
        self.size = (data['Width'], data['Height'])
        self.resize_surface()

    def generate_random_room(self):
        pass

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1920, 1080))
    my_room = Room(RoomType.RECTANGLE, (672, 320))
    my_room.create_room(None)

    stop = False
    while not stop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                stop = True
        
        screen.fill((255, 0, 0))
        my_room.draw(screen)
        pg.display.flip()

    pg.quit()