from os import path
import json
import sys
try:
    from utility import get_path
except ModuleNotFoundError:
    from .utility import get_path

# def get_path(filename):
#     """This is really so that any executables created with pyinstaller can find
#     appropriate resources. Any time a file is read or written, use this
#     function with the relative path from here.
#     """
#     if hasattr(sys, "_MEIPASS"):
#         return path.join(sys._MEIPASS, filename)
#     else:
#         return filename

# This loads the settings into the global scope
if path.isfile(get_path("settings.json")):
    with open(get_path("settings.json"), "r") as settings_file:
        SETTINGS = json.load(settings_file)
else:
    SETTINGS = {
       'General': {
           'FPS': 60,
            'WIDTH': 1280,
            'HEIGHT': 640,
            'FULLSCREEN': False,
            'TILESIZE': 32
       },
       'DEBUG': {
           'LOGGING': True,
           'CLEAR_LOGS': True
       }
    }

    with open(get_path("settings.json"), "w") as settings_file:
        json.dump(SETTINGS, settings_file, indent = 4)