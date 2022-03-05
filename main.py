import pygame as pg
from traceback import format_tb
from os.path import isdir
import sys
import logging
from lib.config import SETTINGS
from lib.utility import get_path
from lib.player import Player
from lib.worldspace import WorldSpace
from lib.room import RoomType
from lib.map_handler.basic_generator import create_files
from lib.dungeon import Dungeon

def log_uncaught_exception(typ, value, traceback):
    """Use to override sys.excepthook to log uncaught exceptions"""
    logging.critical("Uncaught Exception!")
    logging.critical(f"Type: {typ}")
    logging.critical(f"Value: {value}")

    if traceback:
        format_exception = format_tb(traceback)
        for line in format_exception:
            logging.critical(repr(line))

def enable_logging():
    """Enables logging"""
    if SETTINGS['DEBUG']['CLEAR_LOGS']:
        filemode = 'w'
    else:
        filemode = 'a'
    format = f'[%(levelname)s] %(asctime)s %(message)s'
    datefmt='%m/%d/%Y %I:%M:%S %p'
    if SETTINGS['DEBUG']['LOGGING']:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(filename = get_path("debug.log"), encoding = 'utf-8',
                        level = level, filemode = filemode, format = format,
                        datefmt = datefmt)
    logging.info(f'Logging enabled at level {level}')

def event_loop(player, non_walkables, directions, screen, counter = [0]):
    """Monitors all input and performs tasks based on that input."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            logging.info('Detected QUIT event, terminating program.')
            return False
        counter = player_movement(player, event, non_walkables, directions,
                                screen, counter)

    if counter[0] % (SETTINGS['GENERAL']['FPS'] // 4) == 0:
        for direction in directions:
            player.move(direction, screen, non_walkables)
    counter[0] += 1
    return True

def player_movement(player, event, non_walkables, directions, screen,
                    counter):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_UP:
            player.move("up", screen, non_walkables)
            directions.append("up")
            counter[0] = 1
        if event.key == pg.K_DOWN:
            player.move("down", screen, non_walkables)
            directions.append("down")
            counter[0] = 1
        if event.key == pg.K_RIGHT:
            player.move("right", screen, non_walkables)
            directions.append("right")
            counter[0] = 1
        if event.key == pg.K_LEFT:
            player.move("left", screen, non_walkables)
            directions.append("left")
            counter[0] = 1

    if event.type == pg.KEYUP:
        if event.key == pg.K_UP:
            directions.remove("up")
        if event.key == pg.K_DOWN:
            directions.remove("down")
        if event.key == pg.K_RIGHT:
            directions.remove("right")
        if event.key == pg.K_LEFT:
            directions.remove("left")
    return counter

def update_screen(screen, player, space):
    """Draws whatever is supposed to be drawn to the screen."""
    screen.fill((255, 0, 0))
    space.draw(screen)
    player.draw(screen)
    pg.display.flip()

def main():
    """Main loop that runs the whole program"""
    # create_files(get_path(".\\assets\\rooms"))
    clock = pg.time.Clock()
    enable_logging()
    screen_size = (SETTINGS['GENERAL']['WIDTH'], SETTINGS['GENERAL']['HEIGHT'])
    tile_size = SETTINGS['GENERAL']['TILESIZE']
    if SETTINGS['GENERAL']['FULLSCREEN']:
        screen = pg.display.set_mode(screen_size, pg.SRCALPHA, 32, pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode(screen_size, pg.SRCALPHA, 32)

    player = Player((32, 32), (32, 32),
                    get_path(".\\assets\\knight_idle_anim_f0.png"), "Andrew")
    # temp_space = WorldSpace((16, 16), (0, 0))
    # temp_space.create_room(screen, RoomType.RECTANGLE, (8, 8), (0, 0), None)
    # temp_space.create_room(screen, RoomType.ROUND, (8, 8), (7, 0))
    temp_space = WorldSpace((screen_size[0] // tile_size, 
                            screen_size[1] // tile_size), (0, 0))
    # for row in range(0, screen_size[1] // tile_size, 8):
    #     for col in range(0, screen_size[0] // tile_size, 18):
    #         temp_space.create_room(screen, RoomType.ROUND, (18, 8), (col, row))
    temp_dungeon = Dungeon((1, 1), (0, 0), {
        'wall': "assets/wall_1.png",
        'floor': 'assets/floor_1.png'
    })
    non_walkables = pg.sprite.Group()
    temp_space.fix_overlap()
    for cell in temp_space.cells:
        if not cell.is_walkable:
            non_walkables.add(cell)
    
    fps_log_delay = 0
    directions = []
    while event_loop(player, non_walkables, directions, screen):
        update_screen(screen, player, temp_space)
        clock.tick(SETTINGS['GENERAL']['FPS'])
        fps = clock.get_fps()

        # the sole purpose of fps_log_delay is to prevent logs from being
        # generated for the first 10 frames, during which clock.get_fps()
        # returns 0.0
        if fps_log_delay < 10:
            fps_log_delay += 1
        elif fps < SETTINGS['GENERAL']['FPS'] * 0.8:
            logging.warning("Getting a bit too laggy here")
            logging.warning(f"fps recorded at {fps}")

if __name__ == "__main__":
    sys.excepthook = log_uncaught_exception
    pg.init()
    main()
    pg.quit()
    quit()