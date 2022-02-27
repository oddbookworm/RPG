import pygame as pg
try:
    from config import SETTINGS
except ModuleNotFoundError:
    from .config import SETTINGS

class Cell(pg.sprite.Sprite):
    def __init__(self, texture, size: tuple[int], 
                pos: tuple[int], is_walkable: bool = True):
        """world: the pygame.Surface that this Cell is part of
        texture: path to a texture file
        size: tuple of pixels (width, height)
        pos: tuple of pixel offsets from the top-left corner of surface
        """
        super().__init__()
        self.size = size
        self.is_walkable = is_walkable
        self.texture = texture
        self.pos = pos

        self.set_texture(texture)
        self.set_pos(pos)

    def draw(self, screen):
        """draws the Cell to self.world"""
        screen.blit(self.image, self.rect)

    def set_pos(self, new_pos):
        self.pos = new_pos
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def set_texture(self, new_texture):
        """sets the texture"""
        self.texture = new_texture
        with open(self.texture, 'r') as texture:
            self.image = pg.image.load(texture).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.set_pos(self.pos)