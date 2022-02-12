from gameCharacter import GameCharacter

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

            for (key, value) in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    print(f"{type(self).__name__} has no attribute {key}")

            super().__init__(texture = self.texture, pos = self.pos, width = self.width, 
                            height = self.height, interactable = self.interactable, speed = self.speed,
                            repeat = self.repeat, waypoints = self.waypoints)

    def move(self, direction, screen):
        """
        direction: could take on the values of "right", "left", "up", "down"
        """
        screen_size = screen.get_size()

        if direction == "right":
            self.pos = (self.pos[0] + self.speed, self.pos[1])

        elif direction == "left":
            self.pos = (self.pos[0] - self.speed, self.pos[1])
        
        elif direction == "up":
            self.pos = (self.pos[0], self.pos[1] - self.speed)
        
        elif direction == "down":
            self.pos = (self.pos[0], self.pos[1] + self.speed)

        else:
            print(f"{direction} is not a direction name")

        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])
        elif self.pos[0] > screen_size[0] - self.width:
            self.pos = (screen_size[0] - self.width, self.pos[1])

        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)
        elif self.pos[1] > screen_size[1] - self.height:
            self.pos = (self.pos[0], screen_size[1] - self.height)

        self.rect.topleft = self.pos
