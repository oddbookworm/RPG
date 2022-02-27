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

def save_map(width, height, tile_size, cell_list, file_name):
    data = {
        "Textures": {},
        "Width": width,
        "Height": height,
        "Tile Size": tile_size,
        "Floor Layer": [],
        "Collision Layer": []
    }
    textures = {}
    
    i = 0
    for cell in cell_list:
        x, y = cell.pos
        width, height = cell.size
        texture = cell.texture
        if texture not in textures:
            textures[texture] = i
            i += 1

        cell_data = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "texture": textures[texture]
        }

        if cell.is_walkable:
            data["Floor Layer"].append(cell_data)
        else:
            data["Collision Layer"].append(cell_data)

    data["Textures"] = textures

    with open(file_name, "w") as settings_file:
        # json.dump(data, settings_file, indent = 4) # use this one for readability
        json.dump(data, settings_file) # use this one to save space

def save_room(tpl):
    pg.init()
    pg.display.set_mode((1, 1))
    from dummy_cell import Cell
    a = str(Path(__file__).parent.parent.parent.resolve())
    asset_dir = ''.join([a, "\\assets\\"])
    (room_width_tiles, room_height_tiles, tile_size, file_name, style) = tpl
    print((room_width_tiles, room_height_tiles))
    cells = []
    width = room_width_tiles * tile_size
    height = room_height_tiles * tile_size

    if style == "rect":
        for i in range(room_width_tiles):
            for j in range(room_height_tiles):
                texture = asset_dir + "floor_1.png"
                pos = (i * tile_size, j * tile_size)
                size = (tile_size, tile_size)
                cells.append(Cell(texture, size, pos, True))

                if i in [0, room_width_tiles - 1] or j in [0, room_height_tiles - 1]:
                    texture = asset_dir + "wall_1.png"
                    cells.append(Cell(texture, size, pos, False))

    if style == "ellipse":
        a = room_width_tiles / 2 * tile_size
        b = room_height_tiles / 2 * tile_size
        scale_y = a / b
        center = (int(a), int(b))
        for row in range(room_height_tiles):
            for col in range(room_width_tiles):
                pos = (col * tile_size, row * tile_size)
                size = (tile_size, tile_size)
                floor_texture = asset_dir + "floor_1.png"
                wall_texture = asset_dir + "wall_1.png"
                corners = [(col * tile_size, row * tile_size),
                            ((col + 1) * tile_size - 1, row * tile_size),
                            (col * tile_size, (row + 1) * tile_size - 1),
                            ((col + 1) * tile_size - 1, (row + 1) * tile_size - 1)]
                skipping = False
                count = 0
                for i, corner in enumerate(corners):
                    if not skipping:
                        dx = corner[0] - center[0]
                        dy = (corner[1] - center[1]) * scale_y
                        collide = dx * dx + dy * dy < a * a
                        if collide:
                            pos = (col * tile_size, row * tile_size)
                            size = (tile_size, tile_size)
                            count += 1
                            if count > 1:
                                cells.append(Cell(floor_texture, size, pos, True))
                                skipping = True
                        if i == 3 and count <= 1:
                            cells.append(Cell(wall_texture, size, pos, False))

    save_map(width, height, tile_size, cells, file_name)
    pg.quit()