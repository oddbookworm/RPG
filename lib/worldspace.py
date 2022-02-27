import pygame
try:
    from room import Room
    from utility import add_tuples
except ModuleNotFoundError:
    from .room import Room
    from .utility import add_tuples

class WorldSpace:
    def __init__(self, size: tuple[int], pos: tuple[int]):
        """size: tuple of cells (width, height)

        pos: tuple of cells (x, y) offset from the Surface being drawn onto
        """
        self.size = size
        self.pos = pos
        self.rooms = []
        self.cells = []

    def create_room(self, screen, room_type, size, pos, seed = None):
        """screen: the screen to be drawn onto

        room_type: the RoomType that the room will be

        size: the size of the room (in cells)
        
        pos: the position of the room relative to this WorldSpace (in cells)
        """
        room_pos = add_tuples([self.pos, pos])
        room = Room(room_type, size, room_pos)
        room.create_room(seed, screen)
        self.rooms.append(room)
        for cell in room.cells:
            self.cells.append(cell)

    def draw(self, screen: pygame.Surface):
        """draws the space onto screen"""
        # for room in self.rooms:
        #     room.draw(screen)
        for cell in self.cells:
            cell.draw(screen)

    def fix_overlap(self):
        for cell in self.cells:
            for test_cell in self.cells:
                if cell != test_cell:
                    if cell.pos == test_cell.pos:
                        if not cell.is_walkable:
                            self.cells.remove(cell)
                        elif not test_cell.is_walkable:
                            self.cells.remove(test_cell)
    
    def fill_walls(self):
        from copy import deepcopy
        for cell in self.cells:
            if not cell.is_walkable:
                temp = cell
        # need to finish