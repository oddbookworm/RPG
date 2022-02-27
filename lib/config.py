import json
from os import path
try:
    from utility import get_path
except ModuleNotFoundError:
    from .utility import get_path

""" this script loads SETTINGS into the global scope by reading "settings.json"
if it exists, otherwise, creates it and loads default settings"""
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