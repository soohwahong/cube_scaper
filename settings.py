'''
Set settings to use in main and tile class
Returns dictionary where
key: margin, rows, cols, cubeSize, cubeDim, tileDim, levels
value : input values of setting
* max 2000 shapes!
3 faces per tile
tile size = 3*3*3
rows * cols = 4*4*4 

'''



margin = 25
rows, cols = 4, 4
cubeDim = 15
tileSize = 3
tileDim = tileSize * cubeDim
levels = 4

def getSettings():
    S = dict()
    S['margin'] = margin
    S['rows'] = rows
    S['cols'] = cols
    S['cubeDim'] = cubeDim
    S['tileSize'] = tileSize
    S['tileDim'] = tileDim
    S['levels'] = levels
    return S
