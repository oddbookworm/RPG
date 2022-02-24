from enum import Enum, auto
import pygame as pg
from map_handler import loader
from pathlib import Path
import logging
try:
    from cell import Cell
    from config import SETTINGS
except ModuleNotFoundError:
    from .cell import Cell
    from .config import SETTINGS

class WorldSpace:
    def __init__(self, size: tuple[int], pos: tuple[int]):
        """size: tuple of pixels (width, height)
        pos: tuple of pixels (x, y) offset from the Surface being drawn onto
        """
        self.size = size
        self.pos = pos
        self.rooms = []