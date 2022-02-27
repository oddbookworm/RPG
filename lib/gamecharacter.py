import pygame
try:
    from gameobject import GameObject
    from config import SETTINGS
except ModuleNotFoundError:
    from .gameobject import GameObject
    from .config import SETTINGS

class GameCharacter(GameObject):
    def __init__(self, pos: tuple[float], size: tuple[int], texture: str,
                name: str):
        """Initializes the object
        pos: tuple of pixel locations for upper-left corner of object
        size: tuple of pixels (width, height)
        texture: texture path
        name: name for the object
        """
        super().__init__(pos, size, texture)
        self.name = name