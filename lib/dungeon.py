import pygame
import logging
try:
    from worldspace import WorldSpace
    from room import Room, RoomType
    from utility import add_tuples, get_path
    from errors import TilesetKeyError
    from cell import Cell
except ModuleNotFoundError:
    from .worldspace import WorldSpace
    from .room import Room, RoomType
    from .utility import add_tuples, get_path
    from .errors import TilesetKeyError
    from .cell import Cell

class Dungeon(WorldSpace):
    def __init__(self, size: tuple[int], pos: tuple[int],
                    tileset: dict[str, str]):
        """size: tuple of cells (width, height)

        pos: tuple of cells (x, y) offset from the Surface being drawn onto

        tileset: dict of the primary tileset of the dungeon. Required keys are
        'floor' and 'wall' with string values indicating relative location to
        root directory.
        """
        if 'floor' not in tileset.keys() or 'wall' not in tileset.keys():
            if logging.getLogger().hasHandlers():
                logging.critical('Tried to pass in tileset with keys' +
                                f' {tileset.keys()}')
            raise TilesetKeyError

        super().__init__(size, pos)

        floor = get_path(tileset['floor'])
        wall = get_path(tileset['wall'])
        