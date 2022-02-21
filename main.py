import pygame as pg
from os import path
from traceback import format_tb
import sys
import logging
from time import time, localtime, strftime
from lib.config import SETTINGS

def catch_uncaught_exception(typ, value, traceback):
    """Use to override sys.excepthook to log uncaught exceptions"""
    logging.critical("Uncaught Exception!")
    logging.critical(f"Type: {typ}")
    logging.critical(f"Value: {value}")
    # logging.critical(f"Traceback: {traceback}")

    if traceback:
        format_exception = format_tb(traceback)
        for line in format_exception:
            logging.critical(repr(line))

def get_time():
    return strftime("%Y-%m-%d %H:%M:%S", localtime(time()))

def get_path(filename):
    """This is really so that any executables created with pyinstaller can find
    appropriate resources. Any time a file is read or written, use this
    function with the relative path from here.
    """
    if hasattr(sys, "_MEIPASS"):
        return path.join(sys._MEIPASS, filename)
    else:
        return filename

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

def event_loop():
    """Monitors all input and performs tasks based on that input."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            logging.info('Detected QUIT event, terminating program.')
            return False
    return True

def update_screen(screen):
    """Draws whatever is supposed to be drawn to the screen."""
    screen.fill((255, 0, 0))
    pg.display.flip()

def main():
    """Main loop that runs the whole program"""
    clock = pg.time.Clock()
    enable_logging()
    screen_size = (SETTINGS['GENERAL']['WIDTH'], SETTINGS['GENERAL']['HEIGHT'])
    if SETTINGS['GENERAL']['FULLSCREEN']:
        screen = pg.display.set_mode(screen_size, pg.SRCALPHA, 32, pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode(screen_size, pg.SRCALPHA, 32)
    
    fps_log_delay = 0
    while event_loop():
        update_screen(screen)
        clock.tick(SETTINGS['GENERAL']['FPS'])
        fps = clock.get_fps()

        # the sole purpose of fps_log_delay is to prevent logs from being
        # generated for the first 10 frames (during which clock.get_fps())
        # returns 0.0
        if fps_log_delay < 10:
            fps_log_delay += 1
        elif fps < SETTINGS['GENERAL']['FPS'] * 0.8:
            logging.info("Getting a bit too laggy here")
            logging.info(f"fps recorded at {fps}")

if __name__ == "__main__":
    sys.excepthook = catch_uncaught_exception
    pg.init()
    main()
    pg.quit()
    quit()