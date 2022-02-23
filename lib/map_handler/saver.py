import pygame as pg
from pathlib import Path
from sys import path
import logging
import json

# importing from superpkg lib/
_parentdir = Path(__file__).parent.parent.resolve()
path.insert(0, str(_parentdir))

# from cell import Cell

path.remove(str(_parentdir))

def save_map(width, height, tile_size, cell_list):
    data = {
        "Width": width,
        "Height": height,
        "Tile Size": tile_size,
        "Floor Layer": [],
        "Collision Layer": []
    }

    for cell in cell_list:
        x, y = cell.pos
        width, height = cell.size
        texture = cell.texture
        cell_data = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "texture": texture
        }

        if cell.is_walkable:
            data["Floor Layer"].append(cell_data)
        else:
            data["Collision Layer"].append(cell_data)

    with open("E:/Python Scripts/rpg-python/room.json", "w") as settings_file:
        json.dump(data, settings_file, indent = 4)

if __name__ == "__main__":
    pg.init()
    pg.display.set_mode((1,1))
    a = str(Path(__file__).parent.parent.parent.resolve())
    asset_dir = ''.join([a, "\\assets\\"])

    from dummy_cell import Cell
    cells = []

    room_width_tiles = 40
    room_height_tiles = 32
    tile_size = 32
    width = room_width_tiles * tile_size
    height = room_height_tiles * tile_size

    for i in range(room_width_tiles):
        for j in range(room_height_tiles):
            texture = asset_dir + "floor_1.png"
            pos = (i * tile_size, j * tile_size)
            size = (tile_size, tile_size)
            cells.append(Cell(texture, size, pos, True))

            if i in [0, room_width_tiles - 1] or j in [0, room_height_tiles - 1]:
                texture = asset_dir + "wall_1.png"
                cells.append(Cell(texture, size, pos, False))

    save_map(width, height, tile_size, cells)
    pg.quit()