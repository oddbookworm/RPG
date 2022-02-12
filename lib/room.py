from cell import Cell
from enum import Enum, auto

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class RoomType(AutoName):
    RANDOM = auto()
    RECTANGLE = auto()
    ROUND = auto()
    CUSTOM = auto()

class Room:
    def __init__(self, type: RoomType, size: tuple[int]):
        """
        type: one of the values from the RoomType Enum
        size: tuple of pixels (width, height)
        """
        self.type = type
        self.size = size