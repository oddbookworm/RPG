import pygame
import logging
from enum import Enum, auto
from pathlib import Path
try:
    from map_handler import loader
    from config import SETTINGS
    from utility import add_tuples
except ModuleNotFoundError:
    from .map_handler import loader
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

    def create_room(self, seed, screen) -> None:
        """floor_texture: path to a texture

        tile_size: int of tile size

        seed: used to generate a random room
        """
        if not self.__generated:
            self.seed = seed
            if self.room_type == RoomType.RECTANGLE:
                self.__generate_rect_room(screen)
            
            if self.room_type == RoomType.ROUND:
                self.__generate_round_room(screen)

            if self.room_type == RoomType.RANDOM:
                self.__generate_random_room(screen)

            self.__generated = True
        
        else:
            print(f"Room already generated of type {self.room_type}")

    def draw(self, screen) -> None:
        for cell in self.cells:
            cell.draw(screen)
        
    def __generate_rect_room(self, screen) -> None:
        width_tiles = self.size[0]
        height_tiles = self.size[1]
        room_dir = ''.join([str(Path(__file__).parent.parent),
                            "\\assets\\rooms\\rect_rooms\\"])
        room = ''.join([room_dir, f'{width_tiles}x{height_tiles}_rect.json'])
        if logging.getLogger().hasHandlers():
            logging.info(f'Loaded {room} at position {self.pos}')
        # data = loader.load_map(room)
        # self.cells = loader.extract_cells(data, screen)
        # self.size = (data['Width'], data['Height'])

        for row in range(self.size[1]):
            for col in range(self.size[0]):
                if row in [0, self.size[1] - 1] or col in [0, self.size[0] - 1]:
                    pass #wall

                else:
                    pass #floor

        self.offset_cells()

    def __generate_round_room(self, screen) -> None:
        """Generates an elliptical room"""
        width_tiles = self.size[0]
        height_tiles = self.size[1]
        room_dir = ''.join([str(Path(__file__).parent.parent),
                            "\\assets\\rooms\\ell_rooms\\"])
        room = ''.join([room_dir, f'{width_tiles}x{height_tiles}_ell.json'])
        if logging.getLogger().hasHandlers():
            logging.info(f'Loaded {room} at position {self.pos}')
        data = loader.load_map(room)
        self.cells = loader.extract_cells(data, screen)
        self.size = (data['Width'], data['Height'])
        self.offset_cells()

    def __generate_random_room(self, screen) -> None:
        """Not implemented yet"""
        pass

    def offset_cells(self) -> None:
        """Fixes cell positions to be correct on the main window"""
        for cell in self.cells:
            tile_size = SETTINGS['GENERAL']['TILESIZE']
            pos_pixels = (self.pos[0] * tile_size, self.pos[1] * tile_size)
            proper_pos = add_tuples([cell.pos, pos_pixels])
            cell.set_pos(proper_pos)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    my_room = Room(RoomType.RECTANGLE, (672, 320), (100, 50))
    my_room.create_room(None, screen)

    stop = False
    while not stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
        
        screen.fill((255, 0, 0))
        my_room.draw(screen)
        pygame.display.flip()

    pygame.quit()