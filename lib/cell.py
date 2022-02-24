from ast import Mod
import pygame as pg
try:
    from config import SETTINGS
except ModuleNotFoundError:
    from .config import SETTINGS

class Cell(pg.sprite.Sprite):
    def __init__(self, world: pg.Surface, texture, size: tuple[int], 
                pos: tuple[int], is_walkable: bool = True):
        """world: the pygame.Surface that this Cell is part of
        texture: path to a texture file
        size: tuple of pixels (width, height)
        pos: tuple of pixel offsets from the top-left corner of surface
        """
        super().__init__()
        self.world = world
        self.pos = pos
        self.size = size
        self.is_walkable = is_walkable
        self.texture = texture

        self.set_texture(texture)

    def draw(self):
        """draws the Cell to self.world"""
        self.world.blit(self.image, self.rect)

    def swap_world(self, new_world):
        self.world = new_world

    def set_texture(self, new_texture):
        """sets the texture"""
        self.texture = new_texture
        with open(self.texture, 'r') as texture:
            self.image = pg.image.load(texture).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos