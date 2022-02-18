try:
    from gameCharacter import GameCharacter
except ModuleNotFoundError:
    from .gameCharacter import GameCharacter
import pygame as pg

class Player(GameCharacter):
    def __init__(self, **kwargs):
            """
            texture, pos, width, height, interactable: check the constructor of GameObject
            speed: how many pixels per frame should be moved
            waypoints: a list of tuples of pixel positions in order of movement (only major changes)
            repeat: a bool on if the character should 
            """
            self.texture = None
            self.pos = None
            self.width = None
            self.height = None
            self.speed = None
            self.interactable = False
            self.waypoints = None
            self.repeat = False
            self.available = ["right", "left", "up", "down"]
            self.scale = 1
            self.tile_size = None

            for (key, value) in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    print(f"{type(self).__name__} has no attribute {key}")

            super().__init__(texture = self.texture, pos = self.pos, width = self.width, 
                            height = self.height,
                            interactable = self.interactable, speed = self.speed,
                            repeat = self.repeat, waypoints = self.waypoints)

    def collide(self, non_walkables):
        collisions = pg.sprite.spritecollide(self, non_walkables, False)
        for cell in collisions:
            cell_rect = cell.rect
            
            if cell_rect.collidepoint(self.rect.midleft):
                self.pos = (cell.pos[0] + cell.size[0], self.pos[1])
            if cell_rect.collidepoint(self.rect.midright):
                self.pos = (cell.pos[0] - cell.size[0], self.pos[1])

            if cell.rect.collidepoint(self.rect.midtop):
                self.pos = (self.pos[0], cell.pos[1] + cell.size[1])
            if cell.rect.collidepoint(self.rect.midbottom):
                self.pos = (self.pos[0], cell.pos[1] - cell.size[1])

    def move(self, direction, screen, non_walkables):
        """
        direction: could take on the values of "right", "left", "up", "down"
        screen: screen to draw on
        non_walkables: sprite group of non_walkable sprites
        """
        # self.collide(direction, non_walkables)

        old_pos = self.pos

        screen_size = screen.get_size()

        if direction == "right":
            self.pos = (self.pos[0] + self.speed, self.pos[1])
        elif direction == "left":
            self.pos = (self.pos[0] - self.speed, self.pos[1])
        elif direction == "up":
            self.pos = (self.pos[0], self.pos[1] - self.speed)
        elif direction == "down":
            self.pos = (self.pos[0], self.pos[1] + self.speed)

        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])
        elif self.pos[0] > screen_size[0] - self.width:
            self.pos = (screen_size[0] - self.width, self.pos[1])

        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)
        elif self.pos[1] > screen_size[1] - self.height:
            self.pos = (self.pos[0], screen_size[1] - self.height)

        if self.collide(non_walkables):
            self.pos = old_pos

        self.rect.topleft = self.pos
