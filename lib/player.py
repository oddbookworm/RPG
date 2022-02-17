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

            for (key, value) in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    print(f"{type(self).__name__} has no attribute {key}")

            super().__init__(texture = self.texture, pos = self.pos, width = self.width, 
                            height = self.height, interactable = self.interactable, speed = self.speed,
                            repeat = self.repeat, waypoints = self.waypoints)

    def collide(self, non_walkables):
        self.available = ["right", "left", "up", "down"]
        collided = pg.sprite.spritecollideany(self, non_walkables)
        if collided is not None:
            if collided.pos[0] < self.pos[0]:
                self.available.remove("left")
            elif collided.pos[0] > self.pos[0]:
                self.available.remove("right")
            if collided.pos[1] < self.pos[1]:
                self.available.remove("up")
            elif collided.pos[1] > self.pos[1]:
                self.available.remove("down")

    def move(self, direction, screen, non_walkables):
        """
        direction: could take on the values of "right", "left", "up", "down"
        screen: screen to draw on
        non_walkables: sprite group of non_walkable sprites
        """
        screen_size = screen.get_size()

        if direction == "right" and "right" in self.available:
            self.pos = (self.pos[0] + self.speed, self.pos[1])
        elif direction == "left" and "left" in self.available:
            self.pos = (self.pos[0] - self.speed, self.pos[1])
        elif direction == "up" and "up" in self.available:
            self.pos = (self.pos[0], self.pos[1] - self.speed)
        elif direction == "down" and "down" in self.available:
            self.pos = (self.pos[0], self.pos[1] + self.speed)

        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])
        elif self.pos[0] > screen_size[0] - self.width:
            self.pos = (screen_size[0] - self.width, self.pos[1])

        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)
        elif self.pos[1] > screen_size[1] - self.height:
            self.pos = (self.pos[0], screen_size[1] - self.height)

        self.collide(non_walkables)

        self.rect.topleft = self.pos
