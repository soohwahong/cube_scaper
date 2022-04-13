import numpy as np
from settings import getSettings

# settings dictionary where
# key: margin, rows, cols, cubeSize, cubeDim, tileDim, levels
# value : input values of setting
S = getSettings()

class TileSet:
    ''' Create tile set '''
    def __init__(self, name, tile_names):
        self.name = "basic"
        self.tiles_names = ["CUBE", "STAIRS", "HALL"]

class Tile:
    ''' Create tile with adjacency rules'''
    def __init__(self, name):
        self.name = "CUBE"
        self.size = S["tileSize"]
        self.map = np.zeros((self.size, self.size, self.size)) # x, y, z
        # px, py pixel coordinate on canvas
        self.px = -1
        self.py = -1
        # x,y,z coordinate on board
        self.b_x = -1
        self.b_y = -1
        self.b_z = -1
    def setMap(self, arr):
        a_dim = arr.shape
        # print(a_dim)
        if a_dim != (self.size, self.size, self.size):
            raise ValueError(f"array size should be {(self.size, self.size, self.size)}!")
        self.map = arr