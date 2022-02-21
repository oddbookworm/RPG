import pygame as pg
from os import path
import sys
import logging
from lib.config import SETTINGS

def catch_uncaught_exception(typ, value, traceback):
    """Use to override sys.excepthook to log uncaught exceptions"""
    logging.critical("Uncaught Exception!")
    logging.critical(f"Type: {typ}")
    logging.critical(f"Value: {value}")
    logging.critical(f"Traceback: {traceback}")

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
    if SETTINGS['DEBUG']['LOGGING']:
        level = logging.DEBUG
        logging.basicConfig(filename = "debug.log", encoding = 'utf-8', 
                            level = level, filemode = filemode)
    else:
        level = logging.INFO
        logging.basicConfig(filename = "debug.log", encoding = 'utf-8',
                            level = level, filemode = filemode)
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
    while event_loop():
        update_screen(screen)
        clock.tick(SETTINGS['GENERAL']['FPS'])

if __name__ == "__main__":
    sys.excepthook = catch_uncaught_exception
    pg.init()
    main()
    pg.quit()
    quit()