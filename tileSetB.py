import numpy as np
from tile import *

X = TilePattern("X")
Y = TilePattern("Y")
Z = TilePattern("Z")
XY = TilePattern("XY")
YZ = TilePattern("YZ")
XZ = TilePattern("XZ")
XYZ = TilePattern("XYZ")


def resetTileSetB():
        defaultColor = "lightGray"
        X.background = defaultColor
        Y.background = defaultColor
        Z.background = defaultColor
        XY.background = defaultColor
        YZ.background = defaultColor
        XZ.background = defaultColor
        XYZ.background = defaultColor
        return tileSetB

# no rotation allowed!

xFam = [X, XY, XZ, XYZ]
yFam = [Y, XY, YZ, XYZ]
zFam = [Z, XZ, YZ, XYZ]
all  = [X, Y, Z, XY, XZ, YZ, XYZ]
allButY = list(set(all) - set(yFam))
allButX = list(set(all) - set(xFam))
allButZ = list(set(all) - set(zFam))



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
X.adjTop,   X.adjBottom = allButY, allButY
X.adjLeft,  X.adjRight  = xFam, xFam
X.adjAbove, X.adjUnder  = allButZ, allButZ

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
Y.adjLeft,  Y.adjRight  = allButX, allButX
Y.adjAbove, Y.adjUnder  = allButZ, allButZ

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
Z.adjTop,   Z.adjBottom = allButY, allButY
Z.adjLeft,  Z.adjRight  = allButX, allButX
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
XY.adjAbove, XY.adjUnder  = allButZ, allButZ


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

XZ.adjTop,   XZ.adjBottom = allButY, allButY
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
YZ.adjLeft,  YZ.adjRight  = allButX, allButX
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
# tileSetB.tiles = [X, Y, Z, XY, XZ, YZ] # list of tile objects
# tileSetB.tiles = [Y, Z, XZ, YZ] # list of tile objects
# tileSetB.tiles = [XY, XZ, YZ] # list of tile objects


