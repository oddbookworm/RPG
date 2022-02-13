from enum import Enum, auto
import pygame as pg
try:
    from cell import Cell
except ModuleNotFoundError:
    from .cell import Cell

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class RoomType(AutoName):
    RANDOM = auto()
    RECTANGLE = auto()
    ROUND = auto()
    CUSTOM = auto()

class Room:
    def __init__(self, room_type: RoomType, size: tuple[int]):
        """
        room_type: one of the values from the RoomType Enum
        size: tuple of pixels (width, height)
        """
        self.room_type = room_type
        self.size = size
        self.cells = []
        self.image = pg.Surface(self.size, pg.SRCALPHA, 32).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()

    def create_room(self, floor_texture, tile_size):
        if self.room_type == RoomType.RECTANGLE:
            num_horiz_cells = self.size[0] // tile_size
            num_vert_cells = self.size[1] // tile_size
            for row in range(num_vert_cells):
                for col in range(num_horiz_cells):
                    size = (tile_size, tile_size)
                    pos = (col * tile_size, row * tile_size)
                    self.cells.append(Cell(self.image, floor_texture, size,
                                            pos, True))

    def draw(self, pos, screen: pg.Surface):
        self.rect.topleft = pos
        for cell in self.cells:
            cell.draw()
        screen.blit(self.image, self.rect)