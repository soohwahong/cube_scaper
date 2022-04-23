import numpy as np
from tile import *

X = TilePattern("X")
Y = TilePattern("Y")
Z = TilePattern("Z")
XY = TilePattern("XY")
YZ = TilePattern("YZ")
XZ = TilePattern("XZ")
XYZ = TilePattern("XYZ")


# no rotation allowed!

xFam = list([X, XY, XZ, XYZ])
yFam = list([Y, XY, YZ, XYZ])
zFam = list([Z, XZ, YZ, XYZ])
all  = list([X, Y, Z, XY, XZ, YZ, XYZ])


X.map = np.array([
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
        ])
X.adjTop,   X.adjBottom = all, all
X.adjLeft,  X.adjRight  = xFam, xFam
X.adjAbove, X.adjUnder  = all, all

Y.map = np.array([
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
        ])
Y.adjTop,   Y.adjBottom = yFam, yFam
Y.adjLeft,  Y.adjRight  = all, all
Y.adjAbove, Y.adjUnder  = all, all

Z.map = np.array([
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]]
        ])
Z.adjTop,   Z.adjBottom = all, all
Z.adjLeft,  Z.adjRight  = all, all
Z.adjAbove, Z.adjUnder  = zFam, zFam

XY.map = np.array([
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
        ])

XY.adjTop,   XY.adjBottom = yFam, yFam
XY.adjLeft,  XY.adjRight  = xFam, xFam
XY.adjAbove, XY.adjUnder  = all, all


XZ.map = np.array([
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 0]],
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]]
        ])

XZ.adjTop,   XZ.adjBottom = all, all
XZ.adjLeft,  XZ.adjRight  = xFam, xFam
XZ.adjAbove, XZ.adjUnder   = zFam, zFam


YZ.map = np.array([
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]]
        ])

YZ.adjTop,   YZ.adjBottom = yFam, yFam
YZ.adjLeft,  YZ.adjRight  = all, all
YZ.adjAbove, YZ.adjUnder  = zFam, zFam


XYZ.map = np.array([
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]],
        [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]],
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]]
        ])

XYZ.adjTop,   XYZ.adjBottom = yFam, yFam
XYZ.adjLeft,  XYZ.adjRight  = xFam, xFam
XYZ.adjAbove, XYZ.adjUnder  = zFam, zFam

tileSetB = TileSet("B")
tileSetB.tiles = [X, Y, Z, XY, XZ, YZ, XYZ] # list of tile objects


