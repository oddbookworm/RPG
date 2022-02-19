from enum import Enum, auto
import pygame as pg
try:
    from cell import Cell
    from randomRoom import RandomRoom
except ModuleNotFoundError:
    from .cell import Cell
    from .randomRoom import RandomRoom

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class RoomType(AutoName):
    RANDOM = auto()
    RECTANGLE = auto()
    ROUND = auto()
    CUSTOM = auto()
    HALL = auto()

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
        self.entrances = []
        self.exits = []

    def create_room(self, floor_texture, tile_size, seed):
        """
        floor_texture: path to a texture
        tile_size: int of tile size
        seed: only used for random rooms. Use this to duplicate a buggy room
        """
        self.seed = seed
        if self.room_type == RoomType.HALL:
            print("Hall generation handled by Hall subclass")
            print("Use Hall.create_hall() method")
            return

        if self.room_type == RoomType.RECTANGLE:
            self.generate_rect_room(floor_texture, tile_size)
        
        if self.room_type == RoomType.ROUND:
            self.generate_round_room(floor_texture, tile_size)

        if self.room_type == RoomType.RANDOM:
            self.generate_random_room(floor_texture, tile_size)

    def create_walls(self, wall_texture, tile_size):
        floor_positions = [cell.pos for cell in self.cells]
        for row in range(0, self.size[1] // tile_size):
            for col in range(0, self.size[0] // tile_size):
                if (col * tile_size, row * tile_size) not in floor_positions:
                    self.cells.append(Cell(self.image, wall_texture,
                                        (tile_size, tile_size),
                                        (col * tile_size, row * tile_size),
                                        False))

    def draw(self, pos, screen: pg.Surface):
        """
        pos: tuple of pixels relative to screen
        screen: surface to draw onto
        """
        self.rect.topleft = pos
        for cell in self.cells:
            cell.draw()
        screen.blit(self.image, self.rect)
        if self.room_type == RoomType.ROUND:
            pg.draw.ellipse(screen, (0, 255, 0), self.rect, 3)

    def generate_rect_room(self, floor_texture, tile_size):
        num_horiz_cells = self.size[0] // tile_size
        num_vert_cells = self.size[1] // tile_size
        for row in range(num_vert_cells):
            for col in range(num_horiz_cells):
                size = (tile_size, tile_size)
                pos = (col * tile_size, row * tile_size)
                self.cells.append(Cell(self.image, floor_texture, size,
                                        pos, True))
        for cell in self.cells:
            if self.count_floor_neighbors(cell, tile_size) < 4:
                self.entrances.append(cell)
                self.exits.append(cell)

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
                            count += 1
                            if count > 1:
                                self.cells.append(Cell(self.image, floor_texture, size,
                                            pos, True))
                                skipping = True
        
        for cell in self.cells:
            if self.count_floor_neighbors(cell, tile_size) < 4:
                self.entrances.append(cell)
                self.exits.append(cell)

    def count_floor_neighbors(self, cell, tile_size):
        count = 0
        for test_cell in self.cells:
            if test_cell.is_walkable:
                x_dist = abs(cell.pos[0] - test_cell.pos[0])
                y_dist = abs(cell.pos[1] - test_cell.pos[1])
                taxi_dist = x_dist + y_dist
                if taxi_dist == tile_size:
                    count += 1
        return count

    def generate_random_room(self, floor_texture, tile_size):
        random_room = RandomRoom(self.size, tile_size, prob_floor = 0.8, seed = self.seed)
        positions = random_room.floors
        size = (tile_size, tile_size)
        for pos in positions:
            pos = (pos[0] * tile_size, pos[1] * tile_size)
            self.cells.append(Cell(self.image, floor_texture, size, pos, True))