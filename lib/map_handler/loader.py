import pygame
import json
from pathlib import Path
from sys import path

# importing from superpkg lib/
_parentdir = Path(__file__).parent.parent.resolve()
path.insert(0, str(_parentdir))

from cell import Cell

path.remove(str(_parentdir))
# done importing from lib

def load_map(json_file):
    """returns the data from json_file in a dictionary"""
    with open(json_file, "r") as data:
        return json.load(data)

def extract_cells(data, screen):
    """returns a list of cell.Cell objects from data
    screen is the pygame.Surface that the Cells get bound to
    """
    textures = dict((v, k) for k,v in data['Textures'].items())
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
    pygame.init()
    a = str(Path(__file__).parent.parent.parent.resolve())
    asset_dir = ''.join([a, "\\assets\\"])

    # from dummy_cell import Cell

    # data = load_map("E:/Python Scripts/rpygame-python/room_2.json")
    data = load_map("E:/Python Scripts/rpygame-python/assets/rooms/ell_rooms/20x13_ell.json")

    window = pygame.display.set_mode((data['Width'], data['Height']))
    # textures = dict((v, k) for k,v in data['Textures'].items())

    cells = extract_cells(data, window)

    Go = True
    while Go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Go = False

        window.fill((0, 0, 0, 0))
        for cell in cells:
            cell.draw()

        pygame.display.flip()

    pygame.quit()