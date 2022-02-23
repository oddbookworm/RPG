import pygame as pg

class Cell(pg.sprite.Sprite):
    def __init__(self, tex, size: tuple[int], 
                pos: tuple[int], is_walkable: bool = True):
        """A cell that isn't meant to be drawn
        texture: path to a texture file
        size: tuple of pixels (width, height)
        pos: tuple of pixel offsets from the top-left corner of surface
        """
        super().__init__()
        self.pos = pos
        self.size = size
        self.is_walkable = is_walkable
        self.texture = tex

        self.set_texture(tex)

    def set_texture(self, new_texture):
        """sets the texture"""
        self.texture = new_texture
        with open(self.texture, 'r') as texture:
            self.image = pg.image.load(texture).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos