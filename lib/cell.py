import pygame as pg

class Cell(pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, texture, size: tuple[int], pos: tuple[int], is_walkable: bool = True):
        """
        surface: the pygame.Surface that this Cell is part of
        texture: path to a texture file
        size: tuple of pixels (width, height)
        pos: tuple of pixel offsets from the top-left corner of surface
        """
        super().__init__()
        self.surface = surface
        self.pos = pos
        self.size = size
        self.is_walkable = is_walkable

        with open(texture, 'r') as texture:
            self.image = pg.image.load(texture).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        self.surface.blit(self.image, self.rect)