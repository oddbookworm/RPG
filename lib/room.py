from enum import Enum, auto
from math import floor
from numpy import tile
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
            self.generate_rect_room(floor_texture, tile_size)
        
        if self.room_type == RoomType.ROUND:
            self.generate_round_room(floor_texture, tile_size)

    def draw(self, pos, screen: pg.Surface):
        self.rect.topleft = pos
        for cell in self.cells:
            cell.draw()
        screen.blit(self.image, self.rect)
        if self.room_type == RoomType.ROUND:
            pg.draw.ellipse(screen, (0, 255, 0), self.rect, 3)

    def is_corner(self, cell, cells: list[Cell], tile_size):
        horiz = 0
        vert = 0
        for test_cell in cells:
            if test_cell == cell:
                continue
            else:
                if test_cell.pos == (cell.pos[0] + cell.size[0], cell.pos[1]):
                    horiz += 1
                elif test_cell.pos == (cell.pos[0] - cell.size[0], cell.pos[1]):
                    horiz += 1
                elif test_cell.pos == (cell.pos[0], cell.pos[1] + cell.size[1]):
                    vert += 1
                elif test_cell.pos == (cell.pos[0], cell.pos[1] - cell.size[1]):
                    vert += 1
        
        if vert == 1 and horiz == 1:
            return True
        else:
            return False

    def generate_rect_room(self, floor_texture, tile_size):
        num_horiz_cells = self.size[0] // tile_size
        num_vert_cells = self.size[1] // tile_size
        for row in range(num_vert_cells):
            for col in range(num_horiz_cells):
                size = (tile_size, tile_size)
                pos = (col * tile_size, row * tile_size)
                self.cells.append(Cell(self.image, floor_texture, size,
                                        pos, True))

    def generate_round_room(self, floor_texture, tile_size):
        num_horiz_cells = self.size[0] // tile_size
        num_vert_cells = self.size[1] // tile_size
        a = self.size[0] / 2
        b = self.size [1] / 2
        scale_y = a / b
        self.rect = pg.Rect(0, 0, self.size[0], self.size[1])
        self.rect.center = (int(a), int(b))
        for row in range(num_vert_cells):
            for col in range(num_horiz_cells):
                corners = [(col * tile_size, row * tile_size),
                            ((col + 1) * tile_size - 1, row * tile_size),
                            (col * tile_size, (row + 1) * tile_size - 1),
                            ((col + 1) * tile_size - 1, (row + 1) * tile_size - 1)]
                skipping = False
                count = 0
                for corner in corners:
                    if not skipping:
                        dx = corner[0] - self.rect.center[0]
                        dy = (corner[1] - self.rect.center[1]) * scale_y
                        collide = dx * dx + dy * dy < a * a
                        if collide:
                            pos = (col * tile_size, row * tile_size)
                            size = (tile_size, tile_size)
                            # self.cells.append(Cell(self.image, floor_texture, size,
                            #                 pos, True))
                            count += 1
                            if count > 1:
                                self.cells.append(Cell(self.image, floor_texture, size,
                                            pos, True))
                                skipping = True


