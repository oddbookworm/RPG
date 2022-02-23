from ast import Mod
from enum import Enum, auto
import pygame as pg
try:
    from cell import Cell
    from config import SETTINGS
except ModuleNotFoundError:
    from .cell import Cell
    from .config import SETTINGS

class AutoName(Enum):
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
    def __init__(self, room_type: RoomType, size: tuple[int]):
        """room_type: one of the values from the RoomType Enum
        size: tuple of pixels (width, height)
        """
        self.room_type = room_type
        self.size = size
        self.cells = []
        self.image = pg.Surface(self.size, pg.SRCALPHA, 32).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()

    def create_room(self, seed):
        """floor_texture: path to a texture
        tile_size: int of tile size
        seed: only used for random rooms. Use this to duplicate a buggy room
        """
        self.seed = seed
        if self.room_type == RoomType.RECTANGLE:
            self.generate_rect_room()
        
        if self.room_type == RoomType.ROUND:
            self.generate_round_room()

        if self.room_type == RoomType.RANDOM:
            self.generate_random_room()
        
    def generate_rect_room(self):
        pass

    def generate_round_room(self):
        pass

    def generate_random_room(self):
        pass