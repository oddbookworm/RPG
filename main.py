from turtle import color
import pygame as pg
from lib.gameCharacter import GameCharacter
from lib.gameObject import GameObject
from lib.player import Player
from lib.worldSpace import WorldSpace
from lib.room import Room, RoomType

# collision with cells broken: need to fix offsets

def update_screen():
    global screen
    screen.fill(black)
    world_space.draw(screen)
    for object in objects:
        object.draw(screen)
    player.draw(screen)
    pg.display.flip()

def main():
    global screen
    clock = pg.time.Clock()

    fullscreen = False
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_LSHIFT, pg.K_RSHIFT]:
                    player.speed *= 1.75

                if event.key == pg.K_F11:
                    if fullscreen:
                        screen = pg.display.set_mode((win_width, win_height))
                    else:
                        screen = pg.display.set_mode((win_width, win_height),
                                                        pg.FULLSCREEN)
                    fullscreen = not fullscreen

                if event.key == pg.K_UP:
                    player.move("up", screen, world_space.non_walkable)
                if event.key == pg.K_DOWN:
                    player.move("down", screen, world_space.non_walkable)
                if event.key == pg.K_RIGHT:
                    player.move("right", screen, world_space.non_walkable)
                if event.key == pg.K_LEFT:
                    player.move("left", screen, world_space.non_walkable)
            
            if event.type == pg.KEYUP:
                if event.key in [pg.K_LSHIFT, pg.K_RSHIFT]:
                    player.speed /= 1.75
    
        update_screen()

        clock.tick(fps)

def create_objects():
    object_list = []
    default_speed = 3.7 * tile_size / fps # speed of 3.7 tiles per second
    ptex = "assets/knight_idle_anim_f0.png"
    (width, height) = (tile_size, tile_size)
    scale = 0.7
    player = Player(texture = ptex, pos = (32, 32), width = width,
                    height = height, speed = default_speed, scale = scale)

    return object_list, player

def create_space():
    space = WorldSpace((win_width, win_height), tile_size)
    space.create_room((0, 0), (win_width, win_height // 4), 
                        RoomType.RECTANGLE, "assets/floor_1.png")
    space.create_room((0, win_height // 4), (win_width, win_height // 4),
                        RoomType.ROUND, "assets/floor_1.png")
    space.create_room((0, win_height // 2), (win_width, win_height // 2),
                        RoomType.RANDOM, "assets/floor_1.png")
    space.create_walls("assets/wall_1.png")
    return space

if __name__ == "__main__":
    # write function to retrieve from a settings file
    pg.init()

    win_width = 1280
    win_height = 640
    screen = pg.display.set_mode((win_width, win_height))
    tile_size = 32
    fps = 120
    black = (255, 0, 0)

    (objects, player) = create_objects()
    world_space = create_space()

    main()

    pg.quit()
