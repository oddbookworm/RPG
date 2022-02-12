import pygame as pg
from gameObject import GameObject

#     def move(self, new_location):
#         """
#         new_location: a tuple representing the next location to move to
#         """

#     def process_waypoint(self):
#         pass

class GameCharacter(GameObject):
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

        super().__init__(self.texture, self.pos, self.width, self.height, self.interactable)

        if self.waypoints == None:
            self.waypoints = [self.pos]
        self.current_waypoint = self.waypoints[0]

    def move(self, new_location):
        """
        new_location: a tuple representing the next location to move to
        """
        pass

    def process_waypoint(self):
        pass

if __name__ == "__main__":

    def main():
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
        
            update_screen()

    def update_screen():
        screen.fill((0, 0, 255))
        character.draw(screen)
        pg.display.flip()

    pg.init()

    screen = pg.display.set_mode((640, 640))
    tile_size = 32
    fps = 60

    character = GameCharacter(texture = "knight_idle_anim_f0.png", pos = (32, 32), width = 32, height = 32)

    main()

    pg.quit()