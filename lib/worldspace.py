import pygame as pg
from pathlib import Path
import logging
try:
    from cell import Cell
    from config import SETTINGS
    from room import Room, RoomType
except ModuleNotFoundError:
    from .cell import Cell
    from .config import SETTINGS
    from .room import Room, RoomType

class WorldSpace:
    def __init__(self, size: tuple[int], pos: tuple[int]):
        """size: tuple of pixels (width, height)
        pos: tuple of pixels (x, y) offset from the Surface being drawn onto
        """
        self.size = size
        self.pos = pos
        self.rooms = []
        self.cells = []

    def create_room(self, room_type, size, pos, seed = None):
        room = Room(room_type, size, pos)
        room.create_room(seed)
        self.rooms.append(room)
        # don't change the cells
        # for cell in room.cells:
        #     cell.pos = (cell.pos[0] + room.pos[0], cell.pos[1] + room.pos[1])
        #     cell.rect.topleft = cell.pos
        #     self.cells.append(cell)