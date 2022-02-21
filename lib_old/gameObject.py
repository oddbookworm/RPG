import pygame as pg

class GameObject(pg.sprite.Sprite):
    def __init__(self, texture, pos, width, height, interactable = False):
        """
        texture: path to an image to serve as the texture
        pos: tuple of position (in number of pixels)
        width: how many pixels wide the object is
        height: how many pixels tall the object is
        interactable: is the object interactable
        """
        super().__init__()
        with open(texture, 'r') as texture:
            self.image = pg.image.load(texture).convert_alpha()
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.is_interactable = interactable

    def set_interaction(self, interaction):
        """
        interaction should be a callable function
        """
        self.interaction = interaction

    def interact(self, args = ()):
        """
        args should be a tuple of the arguments that the interaction function takes
        """
        self.interaction(args)

    def draw(self, screen):
        """
        screen: the surface to be drawn onto
        """
        screen.blit(self.image, self.rect)