import pygame as pg
from pathlib import Path
from sys import path
import logging
import json
from map_generator import save_room

if __name__ == "__main__":
    from multiprocessing import Pool
    a = str(Path(__file__).parent.parent.parent.resolve())
    asset_dir = ''.join([a, "\\assets\\"])

    from dummy_cell import Cell

    from multiprocessing import Pool
    tile_size = 32
    min_size = 3
    max_size = 40

    args = [(width, height, tile_size, f'C:\\Users\\andre\\Desktop\\maps\\ell_rooms\\{width}x{height}_ell.json', "ellipse") 
            for width in range(min_size, max_size + 1) for height in range(min_size, max_size + 1)]
    
    with Pool(10) as p:
        p.map(save_room, args)

    # save_room((15, 7, tile_size, f'C:\\Users\\andre\\Desktop\\maps\\ell_rooms\\{15}x{7}_ell.json', "ellipse"))