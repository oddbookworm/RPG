try:
    from config import SETTINGS
except ModuleNotFoundError:
    from .config import SETTINGS
import pygame as pg

class GameObject(pg.sprite.Sprite):
    def __init__(self, pos: tuple[float], size: tuple[int], texture: str):
        """Initializes the object
        pos: tuple of pixel locations for upper-left corner of object
        size: tuple of pixels (width, height)
        texture: texture path
        """
        self.size = size
        self.pos = pos

        super().__init__()
        self.set_texture(texture)

    def draw(self, world: pg.Surface):
        """Draws object to the world surface"""
        world.blit(self.image, self.rect)

    def set_texture(self, new_texture):
        with open(texture, 'r') as texture:
            self.image = pg.image.load(texture).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
