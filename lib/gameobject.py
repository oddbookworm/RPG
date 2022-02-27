import pygame
try:
    from config import SETTINGS
except ModuleNotFoundError:
    from .config import SETTINGS

class GameObject(pygame.sprite.Sprite):
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

    def draw(self, world: pygame.Surface) -> None:
        """Draws object to the world surface"""
        world.blit(self.image, self.rect)

    def set_texture(self, texture) -> None:
        """Sets the texture of the GameObject and creates the Rect object"""
        with open(texture, 'r') as texture:
            self.image = pygame.image.load(texture).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
