import pygame as pg
from pprint import pprint
try:
    from cell import Cell
    from room import Room, RoomType
    from graph import Graph
except ModuleNotFoundError:
    from .cell import Cell
    from .room import Room, RoomType
    from .graph import Graph

class Hall(Room):
    def __init__(self, entrance, exit, tile_size):
        """
        entrance and exit are tuples of positions of tiles in pixels
        """
        self.entrance = entrance
        self.entrance_tile = (self.entrance[0] // tile_size,
                                self.entrance[1] // tile_size)
        self.exit = exit
        self.exit_tile = (self.exit[0] // tile_size,
                                self.exit[1] // tile_size)
        self.tile_size = tile_size

        x = min(self.entrance_tile[0], self.exit_tile[0])
        y = min(self.entrance_tile[1], self.exit_tile[1])
        self.entrance_tile = (self.entrance_tile[0] - x, self.entrance_tile[1] - y)
        self.exit_tile = (self.exit_tile[0] - x, self.exit_tile[1] - y)
        size_pixels = (abs(entrance[0] - exit[0]), abs(entrance[1] - exit[1]))
        self.size_tiles = (size_pixels[0] // tile_size, size_pixels[1] // tile_size)

        super().__init__(RoomType.HALL, size_pixels)

    def create_hall(self, floor_tex, wall_tex):
        self.nodes = [self.entrance_tile, self.exit_tile]
        
        for i in range(self.size_tiles[0] + 1):
            for j in range(self.size_tiles[1] + 1):
                self.nodes.append((i, j))

        self.generate_graph()
        self.cells = []
        for pos in self.path:
            new_cell = Cell(self.image, floor_tex, (self.tile_size, self.tile_size),
                            (pos[0] * self.tile_size, pos[1] * self.tile_size), True)
        self.cells.append(new_cell)
        self.create_walls(wall_tex)

    def create_walls(self, wall_tex):
        tile_size = self.tile_size
        floor_positions = [cell.pos for cell in self.cells]
        for row in range(0, self.size[1] // tile_size):
            for col in range(0, self.size[0] // tile_size):
                if (col * tile_size, row * tile_size) not in floor_positions:
                    self.cells.append(Cell(self.image, wall_tex,
                                        (tile_size, tile_size),
                                        (col * tile_size, row * tile_size),
                                        False))


    def generate_graph(self):
        pairs = []
        for node in self.nodes:
            for neighbor in self.get_neighbor_nodes(node):
                pairs.append((node, neighbor))

        g = Graph(connections = pairs)
        print("finding path")
        self.path = g.find_path(self.entrance_tile, self.exit_tile)
        pprint(self.path)
    
    def get_neighbor_nodes(self, node):
        x = node[0]
        y = node[1]
        neighbors = []
        if (x + 1, y) in self.nodes:
            neighbors.append((x + 1, y))
        if (x - 1, y) in self.nodes:
            neighbors.append((x - 1, y))
        if (x, y + 1) in self.nodes:
            neighbors.append((x, y + 1))
        if (x, y - 1) in self.nodes:
            neighbors.append((x, y - 1))
        return neighbors

if __name__ == "__main__":
    screen = pg.display.set_mode((288, 544))
    hall = Hall((64, 128), (256, 512), 32)
    hall.create_hall()