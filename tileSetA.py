import numpy as np
from settings import getSettings
from tile import *

I_h = TileStartEnd("4_3", 4, 3)
I_h.map = np.array([
        [[0, 0, 1],
         [0, 0, 1],
         [0, 0, 1]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
        ])

I_v = TileStartEnd("4_8", 4, 8)
I_v.map = np.array([
        [[0, 0, 1],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 1],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 1],
         [0, 0, 0],
         [0, 0, 0]]
        ])

L_h = TileStartEnd("4_2", 4, 2)
L_h.map = np.array([
        [[0, 0, 1],
         [0, 0, 1],
         [1, 1, 1]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
        ])

L_v = TileStartEnd("4_7", 4, 7)
L_v.map = np.array([
        [[0, 0, 1],
         [0, 0, 1],
         [0, 0, 1]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 1]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 1]]
        ])

Li_v = TileStartEnd("4_7", 4, 7)
Li_v.map = np.array([
        [[0, 0, 1],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 1],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 1],
         [0, 0, 1],
         [0, 0, 1]]
        ])

Lv_Liv = TileStartEnd("4_6", 4, 6)
Lv_Liv.map = np.array([
        [[0, 0, 1],
         [0, 0, 1],
         [0, 0, 1]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 1]],
        [[0, 0, 0],
         [0, 0, 0],
         [1, 1, 1]]
        ])

Lh_Lv = TileStartEnd("4_6", 4, 6)
Lh_Lv.map = np.array([
        [[0, 0, 1],
         [0, 0, 1],
         [1, 1, 1]],
        [[0, 0, 0],
         [0, 0, 0],
         [1, 0, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [1, 0, 0]]
        ])

Lh_Lv_Liv = TileStartEnd("5_4", 5, 4) #flipped
Lh_Lv_Liv.map = np.array([
        [[0, 0, 1],
         [0, 0, 1],
         [1, 1, 1]],
        [[0, 0, 0],
         [0, 0, 0],
         [1, 0, 0]],
        [[1, 0, 0],
         [1, 0, 0],
         [1, 0, 0]]
        ])

empty = TileStartEnd("empty", 0, 0)
empty.map = np.array([
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
        ])

tileSetA = TileSet("A")
tileSetA.tiles = [I_h, I_v, L_h, L_v, Li_v, Lv_Liv, Lh_Lv, Lh_Lv_Liv] # list of tile objects

def constraintToBoard():
        ''' Return dictionary of constraint index : tile coordinate on board'''
        c2b = dict()
        c2b[1] = (0,0,0)
        c2b[2] = (0,2,0)
        c2b[3] = (0,2,2)
        c2b[4] = (0,0,2)
        c2b[5] = (2,0,0)
        c2b[6] = (2,2,0)
        c2b[7] = (2,2,2)
        c2b[8] = (2,0,2)
        # c2b[0] = (None, None, None)
        return c2b

tileSetA.constraintDict = constraintToBoard()

