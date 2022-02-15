try:
    from graph import Graph
    from prng import prng
except ModuleNotFoundError:
    from .graph import Graph
    from .prng import prng
from random import randint

class RandomRoom:
    def __init__(self, size, tile_size, prob_floor = 0.55, seed = None):
        self.size = size
        self.tile_size = tile_size
        self.prob_floor = prob_floor
        if seed == None:
            seed = randint(0, 100000)
        self.seed = seed
        print(f"Generating room with seed {self.seed}")
        (self.walls, self.floors) = self.create_room()
        self.createGraph(self.floors)
        self.getLargestRoom()
        x = [pos[0] for pos in self.floors]
        y = [pos[1] for pos in self.floors]
        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)
        width = max_x - min_x
        height = max_y - min_y
        self.floors = [(pos[0] - min_x, pos[1] - min_y) for pos in self.floors]
        self.size = (width, height)

    def createGraph(self, floors):
        print("Generating graph")
        self.graph = Graph(connections = [], directed = False)
        for cell in floors:
            x = cell[0]
            y = cell[1]
            leftCell = (x - 1, y)
            rightCell = (x + 1, y)
            topCell = (x, y - 1)
            bottomCell = (x, y + 1)
            if leftCell in floors:
                self.graph.add(cell, leftCell)
            if rightCell in floors:
                self.graph.add(cell, rightCell)
            if topCell in floors:
                self.graph.add(cell, topCell)
            if bottomCell in floors:
                self.graph.add(cell, bottomCell)

    def getLargestRoom(self):
        largest = list(self.graph.largest_subgraph())
        removeFromFloor = []
        for cell in self.floors:
            if cell not in largest:
                self.walls.append(cell)
                removeFromFloor.append(cell)
        self.floors = [cell for cell in self.floors if cell not in removeFromFloor]

    def getAdjacentCells(self, cell):
        cells = []
        width = self.size[0] // self.tile_size
        height = self.size[1] // self.tile_size
        x = cell[0]
        y = cell[1]
        if x > 0:
            cells.append((x - 1, y))
        if x < width - 1:
            cells.append((x + 1, y))
        if y > 0:
            cells.append((x, y - 1))
        if y < height - 1:
            cells.append((x, y + 1))
        if x > 0 and y > 0:
            cells.append((x - 1, y - 1))
        if x > 0 and y < height - 1:
            cells.append((x - 1, y + 1))
        if x < width - 1 and y > 0:
            cells.append((x + 1, y - 1))
        if x < width - 1 and y < height - 1:
            cells.append((x + 1, y + 1))
        return cells
    
    def create_room(self):
        width = self.size[0] // self.tile_size
        height = self.size[1] // self.tile_size
        random_numbers = prng(self.seed, width * height)
        floors = []
        walls = []
        for column in range(width):
            for row in range(height):
                if random_numbers[row + column * height] < self.prob_floor and row > 0 and row < height - 1 and column > 0 and column < width - 1:
                    floors.append((column, row))
                else:
                    walls.append((column, row))

        print("Rough rooms generated\nSmoothing things out")
        i = 0
        while i < 5:
            number_changes = 0
            print(f"Iteration {i + 1} of smoothing")
            added_floors = []
            added_walls = []
            i += 1
            change = False
            for cell in floors:
                adjacent = self.getAdjacentCells(cell)
                adjacentFloors = list(set(adjacent).intersection(set(floors)))
                if len(adjacentFloors) < 4:
                    # walls.append(cell)
                    # floors.remove(cell)
                    added_walls.append(cell)
                    number_changes += 1
            
            for cell in walls:
                adjacent = self.getAdjacentCells(cell)
                adjacentFloors = list(set(adjacent).intersection(set(floors)))
                if len(adjacentFloors) > 6:
                    # floors.append(cell)
                    # walls.remove(cell)
                    added_floors.append(cell)
                    number_changes += 1
            
            floors = [cell for cell in set(floors).union(set(added_floors)) if cell not in added_walls]
            walls = [cell for cell in set(walls).union(set(added_walls)) if cell not in added_floors]
            print(f"{number_changes} change(s) made this iteration")
            
        print("Candidate rooms generated")
        return (walls, floors)