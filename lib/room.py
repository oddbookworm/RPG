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
    from utility import add_tuples
except ModuleNotFoundError:
    from .cell import Cell
    from .config import SETTINGS
    from .utility import add_tuples

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
    def __init__(self, room_type: RoomType, size: tuple[int],
                pos: tuple[int] = (0, 0)):
        """room_type: one of the values from the RoomType Enum
        size: tuple of cells (width, height)
        pos: tuple of cells (x, y) offset from the Surface being drawn onto
        """
        self.room_type = room_type
        self.size = size
        self.pos = pos
        self.cells = []
        self.__generated = False

    def create_room(self, seed, screen):
        """floor_texture: path to a texture
        tile_size: int of tile size
        seed: used to generate a random room
        """
        if not self.__generated:
            self.seed = seed
            if self.room_type == RoomType.RECTANGLE:
                self.generate_rect_room(screen)
            
            if self.room_type == RoomType.ROUND:
                self.generate_round_room(screen)

            if self.room_type == RoomType.RANDOM:
                self.generate_random_room(screen)

            self.__generated = True
        
        else:
            print(f"Room already generated of type {self.room_type}")

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)
        
    def generate_rect_room(self, screen):
        width_tiles = self.size[0]
        height_tiles = self.size[1]
        room_dir = ''.join([str(Path(__file__).parent.parent),
                            "\\assets\\rooms\\rect_rooms\\"])
        room = ''.join([room_dir, f'{width_tiles}x{height_tiles}_rect.json'])
        logging.info(f'Loaded {room} at position {self.pos}')
        data = loader.load_map(room)
        self.cells = loader.extract_cells(data, screen)
        self.size = (data['Width'], data['Height'])
        self.offset_cells()

    def generate_round_room(self, screen):
        width_tiles = self.size[0]
        height_tiles = self.size[1]
        room_dir = ''.join([str(Path(__file__).parent.parent),
                            "\\assets\\rooms\\ell_rooms\\"])
        room = ''.join([room_dir, f'{width_tiles}x{height_tiles}_ell.json'])
        logging.info(f'Loaded {room} at position {self.pos}')
        data = loader.load_map(room)
        self.cells = loader.extract_cells(data, screen)
        self.size = (data['Width'], data['Height'])
        self.offset_cells()

    def generate_random_room(self, screen):
        pass

    def offset_cells(self):
        for cell in self.cells:
            tile_size = SETTINGS['GENERAL']['TILESIZE']
            pos_pixels = (self.pos[0] * tile_size, self.pos[1] * tile_size)
            proper_pos = add_tuples([cell.pos, pos_pixels])
            cell.set_pos(proper_pos)

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1920, 1080))
    my_room = Room(RoomType.RECTANGLE, (672, 320), (100, 50))
    my_room.create_room(None, screen)

    stop = False
    while not stop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                stop = True
        
        screen.fill((255, 0, 0))
        my_room.draw(screen)
        pg.display.flip()

    pg.quit()