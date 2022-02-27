import pygame as pg
from pathlib import Path
from sys import path
import logging

# importing from superpkg lib/
_parentdir = Path(__file__).parent.parent.resolve()
path.insert(0, str(_parentdir))

from cell import Cell

path.remove(str(_parentdir))

class Rectangular:
    pass