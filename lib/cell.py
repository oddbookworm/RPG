import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, texture, size: tuple[int], 
                pos: tuple[int], is_walkable: bool = True):
        """texture: path to a texture file

        size: tuple of pixels (width, height)

        pos: tuple of pixel offsets from the top-left corner of parent Surface
        """
        super().__init__()
        self.size = size
        self.is_walkable = is_walkable
        self.texture = texture
        self.pos = pos

        self.set_texture(texture)
        self.set_pos(pos)

    def draw(self, screen) -> None:
        """draws the Cell to self.world"""
        screen.blit(self.image, self.rect)

    def set_pos(self, new_pos) -> None:
        """sets the position of the Cell"""
        self.pos = new_pos
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def set_texture(self, new_texture: str) -> None:
        """sets the texture of the Cell"""
        self.texture = new_texture
        with open(self.texture, 'r') as texture:
            self.image = pygame.image.load(texture).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
