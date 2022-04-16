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
        self.name = name
        self.size = S["tileSize"]
        self.map = np.zeros((self.size, self.size, self.size)) # z, y, x should be z, x, y!
        # px, py pixel coordinate of center of tile : to move and place tile
        self.px = -1
        self.py = -1
        # x,y,z coordinate on board
        self.onBoard = False # if moving on board, snaps to board, else draw on pixel coordinate
        self.l = -1
        self.r = -1
        self.c = -1
        # rotation status
        self.rotated = 0

    def __repr__(self):
        return f'{self.name}({self.rotated})'

    def setMap(self, arr):
        a_dim = arr.shape
        # print(a_dim)
        if a_dim != (self.size, self.size, self.size):
            raise ValueError(f"array size should be {(self.size, self.size, self.size)}!")
        self.map = arr

    def rotate(self):
        '''rotate tile counter clockwise'''
        # self.map = np.rot90(self.map, 1, (2,1))
        self.map = np.rot90(self.map, 1, (1,2)) # clockwise
        self.rotated += 1