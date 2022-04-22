import numpy as np
from settings import getSettings
from tile import *

X = Tile("X")
Y = Tile("Y")
Z = Tile("Z")
XY = Tile("XY")
YZ = Tile("YZ")
XZ = Tile("XZ")
XYZ = Tile("XYZ")

xFam = [X, XY, XZ, XYZ]
yFam = [Y, XY, YZ, XYZ]
zFam = [Z, XZ, YZ, XYZ]

X.map = np.array([
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
X.adjTop,   X.adjBottom = [], [] 
X.adjLeft,  X.adjRight  = xFam, xFam
X.adjAbove, X.adjBelow  = [], []

Y.map = np.array([
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
Y.adjTop,   Y.adjBottom = yFam, yFam
Y.adjLeft,  Y.adjRight  = [], []
Y.adjAbove, Y.adjBelow  = [], []

Z.map = np.array([
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
Z.adjTop,   Z.adjBottom = [], []
Z.adjLeft,  Z.adjRight  = [], []
Z.adjAbove, Z.adjBelow  = zFam, zFam

XY.map = np.array([
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

XY.adjTop,   XY.adjBottom = yFam, yFam
XY.adjLeft,  XY.adjRight  = xFam, xFam
XY.adjAbove, XY.adjBelow  = [], []


XZ.map = np.array([
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

XZ.adjTop,   XZ.adjBottom = [], []
XZ.adjLeft,  XZ.adjRight  = xFam, xFam
XZ.adjAbove, XZ.adjBelow  = zFam, zFam


YZ.map = np.array([
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

YZ.adjTop,   YZ.adjBottom = yFam, yFam
YZ.adjLeft,  YZ.adjRight  = [], []
YZ.adjAbove, YZ.adjBelow  = zFam, zFam


XYZ.map = np.array([
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

XYZ.adjTop,   XYZ.adjBottom = yFam, yFam
XYZ.adjLeft,  XYZ.adjRight  = xFam, xFam
XYZ.adjAbove, XYZ.adjBelow  = zFam, zFam

tileSetB = TileSet("B")
tileSetB.tiles = [X, Y, Z, XY, XZ, YZ, XYZ] # list of tile objects


