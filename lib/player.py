import pygame as pg
import logging
try:
    from gamecharacter import GameCharacter
    from config import SETTINGS
    from utility import add_tuples
except ModuleNotFoundError:
    from .gamecharacter import GameCharacter
    from .config import SETTINGS
    from .utility import add_tuples

class Player(GameCharacter):
    def __init__(self, pos: tuple[float], size: tuple[int], texture: str,
                name: str = "Player"):
        """Initializes the player
        pos: tuple of pixel locations for upper-left corner of object
        size: tuple of pixels (width, height)
        texture: texture path
        name: name for the object, defaults to "Player"
        """
        super().__init__(pos, size, texture, name)

    def collide(self, non_walkables: pg.sprite.Group):
        """returns True if Player collides with any sprite in non_walkables
        else returns False
        """
        return pg.sprite.spritecollideany(self, non_walkables)

    def move(self, direction: str, world: pg.Surface,
                non_walkables: pg.sprite.Group):
        """Moves the player one tile based on direction. Does not let player
        leave the world. Also handles collision with non_walkables.
        """
        world_size = world.get_size()

        old_pos = self.pos

        options = {
            'right': (self.size[0], 0),
            'left': (-self.size[0], 0),
            'up': (0, -self.size[1]),
            'down': (0, self.size[1])
        }

        self.pos = add_tuples(self.pos, options[direction])

        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])
        elif self.pos[0] > world_size[0] - self.width:
            self.pos = (world_size[0] - self.width, self.pos[1])

        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)
        elif self.pos[1] > world_size[1] - self.height:
            self.pos = (self.pos[0], world_size[1] - self.height)

        self.rect.topleft = self.pos

        if self.collide(non_walkables):
            self.pos = old_pos
            self.rect.topleft = self.pos