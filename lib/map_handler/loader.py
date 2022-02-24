import pygame as pg
from pathlib import Path
from sys import path
import logging
import json
from time import perf_counter

# importing from superpkg lib/
_parentdir = Path(__file__).parent.parent.resolve()
path.insert(0, str(_parentdir))

from cell import Cell

path.remove(str(_parentdir))

def load_map(json_file):
    with open(json_file, "r") as data:
        return json.load(data)

def extract_cells(data, screen, textures):
    cells = []
    for cell in data['Floor Layer']:
        texture = textures[cell['texture']]
        size = (cell['width'], cell['height'])
        pos = (cell['x'], cell['y'])
        try:
            cells.append(Cell(screen, texture, size, pos, True))
        except Exception:
            cells.append(Cell(texture, size, pos, True))

    for cell in data['Collision Layer']:
        texture = textures[cell['texture']]
        size = (cell['width'], cell['height'])
        pos = (cell['x'], cell['y'])
        try:
            cells.append(Cell(screen, texture, size, pos, False))
        except Exception:
            cells.append(Cell(texture, size, pos, False))
    return cells

if __name__ == "__main__":
    pg.init()
    a = str(Path(__file__).parent.parent.parent.resolve())
    asset_dir = ''.join([a, "\\assets\\"])

    # from dummy_cell import Cell

    # data = load_map("E:/Python Scripts/rpg-python/room_2.json")
    data = load_map("C:/Users/andre/Desktop/maps/ell_rooms/20x13_ell.json")

    window = pg.display.set_mode((data['Width'], data['Height']))
    textures = dict((v, k) for k,v in data['Textures'].items())

    cells = extract_cells(data, window, textures)

    Go = True
    while Go:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Go = False

        window.fill((0, 0, 0, 0))
        for cell in cells:
            cell.draw()

        pg.display.flip()

    pg.quit()