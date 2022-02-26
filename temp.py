from temp_config import *

class GameState:
    def __init__(self, game):
        self.game = game
        self.game_state = 'load_map'
    
    def load_map(self):
        global tilemap
        if tilemap == None:
            tilemap = "TEST"

print(tilemap)
gs = GameState("blah")
gs.load_map()

print(tilemap)