from concurrent.futures.process import _threads_wakeups
from operator import truediv
from cmu_cs3_graphics import *
import numpy as np
import settings 
import copy
from matplotlib import path
import random
from tile import *
from tileSetB import *
from isometric import *

''' Resources 
    1. Isometric Projection
    https://www.youtube.com/watch?v=gE2gTCwLdFM
    https://k3no.medium.com/isometric-grids-in-python-40c0fad54552
    https://tips.clip-studio.com/en-us/articles/4969
    
    2. Isometric Tile Set
    http://cr31.co.uk/iso/iso.html
    https://catlikecoding.com/unity/tutorials/marching-squares/

    3. Other
    InPolygon :  https://stackoverflow.com/questions/31542843/inpolygon-examples-of-matplotlib-path-path-contains-points-method
    Rotation : https://appdividend.com/2022/01/13/numpy-rot90/
    Numpy: https://stackoverflow.com/questions/4877624/numpy-array-of-objects
    '''


def onAppStart(app):
    S = settings.getSettings()
    app.margin = S["margin"]

    # Tile & Cube
    app.tileSize = S["tileSize"] # num of cubes on one side of tile
    app.cubeDim = S["cubeDim"]   # pixel dim of one side of cube 
    app.tileDim = app.tileSize * app.cubeDim   # pixel dim of one side of tile
    app.tileSet = tileSetB

    # Tile set window (width, height, left, top)
    app.tileWin_w = app.width/2 - 5 * app.margin
    app.tileWin_h = app.height - 3 * app.margin
    app.tileWin_l = app.margin
    app.tileWin_t = 2*app.margin

    # Iso board window (width, height, left, top)
    app.gridWin_w = app.width/2 + 2 * app.margin 
    app.gridWin_h = app.height - 3 * app.margin
    app.gridWin_l = app.width/ 2 - 3 * app.margin
    app.gridWin_t = 2*app.margin

    # Iso board
    app.rows, app.cols= S["rows"], S["cols"]
    app.levels = S["levels"]
    # cube unit board
    app.board = np.zeros((app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize)) 
    # tile unit board : stores tile objects
    app.board_tiles = np.empty((app.levels, app.rows, app.cols), dtype=object)
    # records number of rotations counter clockwise of board. 
    # 0 is default 0~3
    app.board_rotated = 0
    
    # Top pixel coordinate of background grid at level 0
    app.grid_ix, app.grid_iy = app.gridWin_l + app.gridWin_w/2, app.gridWin_t + app.tileDim * (app.levels + 2)

    # User action state
    app.holdingTile = False
    app.currentTile = None

    # level guide
    app.currentLevel = 0
    app.levelGuide = True

    # Path Finding
    app.pathMode = False # differentiate between pattern and path mode
    app.pathFinding = False
    app.settingSTART = False
    app.settingEND = False
    app.START = None # cube index of center of home tile 
    app.END = None # cube index of center of dest tile
    app.pathFound = []
    app.pathMap = np.zeros((app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize))

    # Pattern Finding with WFC
    app.patternMode = False
    app.outputBoard = dict() # dictionary of list of what tiles can come based on adjacency rules 
    initOutputBoard(app)
    app.foundPattern = False

    # Selecting subset of tiles
    app.selectTileSet = False
    app.modifiedTileSet = TileSet("mod_tileSetB")

    # UI Features
    app.status = ""
    app.startScreen = True


## Functions used on start
def initOutputBoard(app):
    '''dictionary where
        key = (l,r,c) tuple of coordinate on board
        value = list of all tile types, initialized as empty list'''
    output = dict()
    for l in range(app.levels):
        for r in range(app.rows):
            for c in range(app.cols):
                output[(l,c,r)] = copy.deepcopy(app.tileSet.tiles)
    app.outputBoard = output


## Controllers
def onKeyPress(app, key):
    if app.startScreen:
        if key == '1': # path finding mode
            app.pathMode = True
            app.patternMode = False
            app.tileSet = tileSetB
            app.startScreen = False

        elif key == '0': # pattern finding mode
            app.patternMode = True
            app.pathMode = False
            app.tileSet = tileSetB
            app.startScreen = False
    else:
        # Rotate Holding tile
        # if app.holdingTile:
        #     if key.lower() == 't':
        #         app.currentTile.rotate()

        # Control Level guide
        if (key == 'up') and (app.currentLevel<app.levels-1):
            app.currentLevel += 1
        if (key == 'down') and (app.currentLevel>0):
            app.currentLevel -= 1
        if key.lower() == 'l':
            app.levelGuide = not app.levelGuide

        # Rotate board
        if (key == 'right'):
            rotateBoard(app)

        # Setting start
        if (key.lower() == 's'):
            app.settingSTART = True
            app.settingEND = False
        
        if key.lower() == 'e':
            app.settingEND = True
            app.settingSTART = False

        if key.lower() == 'p':
            res = isPath(app)
            app.pathFinding = True
            if res == None:
                pass
            else:
                app.pathFound = res 

        if key.lower() == 'r':
            clearBoard(app)
            # if app.patternMode:
            app.tileSet = resetTileSetB() # reset tileSet
            app.modifiedTileSet.tiles = [] # reset modified tileSet
            app.foundPattern = False

        if key.lower() == 'w':
            if app.patternMode:
                patternGenerate(app)

        if key.lower() == 'z':
            if app.patternMode:
                app.selectTileSet = not app.selectTileSet # switch modes on and off
                
                if app.selectTileSet:
                    pass
                if app.selectTileSet == False: # finalize tile set
                    # revert background color
                    for tile in app.modifiedTileSet.tiles:
                        tile.background = "lightGray" 
                    app.tileSet = copy.deepcopy(app.modifiedTileSet)
                    # reduce outputBoard to tileSet
                    for l in range(app.levels):
                        for r in range(app.rows):
                            for c in range(app.cols):
                                app.outputBoard[(l,r,c)] = copy.deepcopy(app.tileSet.tiles)

        if key.lower() == 'h':
            clearBoard(app)
            app.startScreen = True

def clearBoard(app):
    app.holdingTile = False
    app.currentTile = None
    app.board_tiles = np.empty((app.levels, app.rows, app.cols), dtype=object)
    app.board = np.zeros((app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize)) 
    
    # path finding mode
    app.pathFinding = False
    app.settingSTART = False
    app.settingEND = False
    app.START = None
    app.END = None
    app.pathFound = []
    app.pathMap = np.zeros((app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize)) 
    
    # if app.patternMode:
    initOutputBoard(app)    

def rotateBoard(app):
    ''' On right press, rotate the board
        '''
    app.board = np.rot90(app.board, 1, (1,2))
    app.board_rotated = (app.board_rotated+1)%4
    app.pathMap = np.rot90(app.pathMap, 1, (1,2))

def onMousePress(app, mouseX, mouseY):
    # tile selecting mode in pattern mode on key press 's'
    if app.patternMode and app.selectTileSet:
        select = isTileSelect(app, mouseX, mouseY)
        for tile in app.tileSet.tiles:
            if select == tile: tile.background = "red"
        if select != None:
            if select not in app.modifiedTileSet.tiles:
                app.modifiedTileSet.tiles.append(select)
        
    elif not app.holdingTile: # not holding tile
        # Case 1: Selecting tile anew to add to board
        select = isTileSelect(app, mouseX, mouseY)
        if select != None:
            app.holdingTile = True
            app.currentTile = select

    else: # holding tile
        select = isTileSelect(app, mouseX, mouseY) # checks if click is in tileset region
        # Case 2: swap holding tile
        if select !=None:
            app.currentTile = select
        
        # Case 2: drop tile if click not in board or tile select
        elif inBoardRegion(app, mouseX, mouseY) == None: 
            app.holdingTile = False
            app.currentTile.onBoard = False
            app.currentTile = None

        # Case 3: Place current tile on board if legal 
        else:
            if isTileLegalOnBoard(app, app.currentTile, app.currentTile.l, app.currentTile.r, app.currentTile.c):
                placeTileOnBoard(app, app.currentTile, app.currentTile.l, app.currentTile.r, app.currentTile.c)
                # if setting home, placed tile is home
                if app.settingSTART:
                     # get cube index of center of tile
                    app.START = getTileCenterCubeInd(app, app.currentTile)
                if app.settingEND:
                    app.END = getTileCenterCubeInd(app, app.currentTile)
                app.settingSTART = False
                app.settingEND = False

                # revert app attributes related to holding tile
                app.currentTile = None
                app.holdingTile = False

def onMouseMove(app, mouseX, mouseY):
    if app.holdingTile:
        # if in board region, snap to board 
        if (inBoardRegion(app, mouseX, mouseY)!=None):
            # set tile attributes
                # set on board to true
            app.currentTile.onBoard = True
                # set tile location to snap to board
            l, r, c = inBoardRegion(app, mouseX, mouseY) # board coordinate of tile
            app.currentTile.l, app.currentTile.r, app.currentTile.c = l, r, c
            app.currentTile.px, app.currentTile.py = tileIndexToPixel(app,l,r,c)

        # if not in board region, draw on mouse
        else:
            # set tile attributes
            # set on board to false
            app.currentTile.onBoard = False
            app.currentTile.l, app.currentTile.r, app.currentTile.c = -1, -1, -1
            # set tile location to mouse
            # draw *above side left cube* of current tile on mouse position(to visualize better!)
            app.currentTile.px, app.currentTile.py = mouseX+app.tileDim, mouseY-app.tileDim//2

def isTileSelect(app, mouseX, mouseY):
    ''' Checks if click is on any tile in tile set window,
        and if it is, returns copy of clicked tile,
        otherwise return None'''
    for tile in app.tileSet.tiles:
        if ((tile.px-app.tileDim < mouseX < tile.px+app.tileDim)
            and (tile.py-app.tileDim < mouseY < tile.py+app.tileDim)):
            selected_tile = copy.deepcopy(tile)
            return selected_tile
    return None

def inBoardRegion(app, mouseX, mouseY):
    ''' Checks if mouse is on isometric board window,
        and if it is, returns tile index (level, row, col),
        otherwise return None'''
    # for each index in board
    # for l, r, c in np.argwhere(app.board_tiles!=0): # get all indices of board tile
    for l, r, c in np.argwhere(app.board_tiles[app.currentLevel:app.currentLevel+1]!=0): # get all indices of board tile
        # get four corners pixel coordinates in order t, r, b, l
        d = app.tileDim
        tx ,ty = tileIndexToPixel(app,app.currentLevel,r,c)
        rx, ry = tx+d, ty-0.5*d
        bx, by = tx, ty+d
        lx, ly = tx-d, ty-0.5*d
        
        xv = np.array([tx, rx, bx, lx])
        yv = np.array([ty, ry, by, ly])
        if inPolygon(np.array([mouseX]), np.array([mouseY]), xv, yv):
            return app.currentLevel, r, c

def isTileLegalOnBoard(app, tile, l, r, c):
    ''' Given tile and tile index on board, 
        Returns boolean value of whether tile is legal 
        (there isn't any existing tile on board
        and meets adjacency constraints with neighboring tiles (3 previous, 3 next tiles)
        Used in mousePress, DrawTileOnBoard'''
    # Checks existing
    if app.board_tiles[l,r,c] != None: return False
    # Checks adjacency
    if tile not in app.outputBoard[(l,r,c)]:
        return False
    return True

def inPolygon(xq, yq, xv, yv):
        ''' xv, yv are 1d numpy arrays of coordinates that form polygon
            xq, yq are 1d numpy arrays of points that are being evaluated
            returns 1d array of boolean values
            Author : Ramesh-X
            Date: Apr 9, 2018
            Availability: https://stackoverflow.com/questions/31542843/inpolygon-examples-of-matplotlib-path-path-contains-points-method
            '''
        shape = xq.shape
        xq = xq.reshape(-1) 
        yq = yq.reshape(-1)
        xv = xv.reshape(-1)
        yv = yv.reshape(-1)
        q = [(xq[i], yq[i]) for i in range(xq.shape[0])]
        p = path.Path([(xv[i], yv[i]) for i in range(xv.shape[0])])
        return p.contains_points(q).reshape(shape)

## Index to Pixel Functions ##
def tileIndexToPixel(app, l, r, c):
    '''Given 3d board coordinate of tile unit l, c, r,
    Return pixel coordinate of origin point(center) tx, ty
    isometric width is 2*tileDim and height is 1*tileDim
    Make sure that pixel value is integer!
    '''
    d = app.tileDim
    tx = app.grid_ix + r*d - c*d 
    ty = app.grid_iy + r*0.5*d + c*0.5*d - l*d
    return tx, ty

def getTileCenterCubeInd(app, tile):
    '''Given tile, take its l,r,c index on board and return center (1,1,1) cube index z,x,y on board'''
    d = app.tileSize
    z, x, y = tile.l*d, tile.r*d, tile.c*d
    return (z+1, x+1, y+1)

def cubeIndexToPixel(app, z, x, y):
    '''Given 3d board coordinate of cube unit z, y, x
    Return pixel coordinate of origin point(center) cx, cy
    isometric width is 2*cubeDim and height is 1*cubeDim
    Make sure that pixel value is integer!
    '''
    d = app.cubeDim
    cx = app.grid_ix + x*d - y*d 
    cy = app.grid_iy + x*0.5*d + y*0.5*d - z*d
    return cx, cy

def onStep(app):
    setStatusBar(app)
    if not app.startScreen:
        assert(app.patternMode != app.pathMode)

def drawPath(app):
    d = app.cubeDim
    cubeInds = np.argwhere(app.pathMap == 1)
    for cube in cubeInds:
        z, x, y = cube
        # cx, cy : pixel coordinate of cube origin (above top)
        cx, cy = cubeIndexToPixel(app, z, x, y)

        ## integrating drawIsoCube(t_ix, t_iy, d, d, d) so that draw less shapes
        tt, tr, tb, tl = getCornerPointsIsoRect(cx, cy-d, d, d)
        bt, br, bb, bl = getCornerPointsIsoRect(cx, cy, d, d)

        # Draw all 3 faces
        drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='lightCoral', opacity=40) # draw top    
        drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='fireBrick', opacity=40) # draw left front
        drawPolygon(*tb, *tr, *br, *bb, border='black', borderWidth=0.3, fill='darkRed', opacity=40) # draw right front

def setStatusBar(app):
    ''' Writes messages and status of game on top of page'''
    # default
    if app.pathMode:
        app.status = "Press S and select and place START tile       Press E and select and place END tile       Press P to generate PATH"
        if app.settingSTART:
            app.status = "Select a START tile rotate and drop it on the board"
        if app.settingEND:
            app.status = "Select a END tile rotate and drop it on the board"
        if app.pathFinding:
            if len(app.pathFound) == 0:
                app.status = "Path not found. Try drawing again."
            else: 
                app.status = "We found a path!"
            
    if app.patternMode:
        app.status = "Press Z to select tiles       Press W to generate 3d PATTERN"
        if app.foundPattern:
            app.status = "Generated full board!"
        if app.selectTileSet:
            app.status = "Click on tiles to add to your set     Press Z when done adding"
    
## Draw ##
def redrawAll(app):
    drawTileSet(app)
    drawGrid(app)        
    drawBoard(app) 
    drawLevelGuide(app)
    drawMovingTile(app)
    drawStatusBar(app)
    drawStationaryText(app)
    if app.pathFound:
        drawPath(app)
    if app.startScreen:
        drawStartScreen(app)

def drawStartScreen(app):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=70)
    drawLabel("CUBE SCAPER", app.width//2, app.height//2-75, size=40, fill='white', font='montserrat', align='center', italic=True)
    drawLabel("What are we scaping?", app.width//2, app.height//2, size=24, fill='white', font='montserrat', align='center', italic=True)
    drawLabel("0: Pattern        1: Path", app.width//2, app.height//2+50, size=24, fill='white', font='montserrat', align='center')
    
def drawStatusBar(app):
    drawLabel(app.status, app.width-30, 30, size=14, font='montserrat', fill='darkOrange', align='right', italic=True)
    if app.startScreen:
        drawLabel("HELLO", 35, 30, size=16, font='montserrat', align='left')
    elif app.pathMode:
        drawLabel("PATH MODE", 35, 30, size=16, font='montserrat', align='left')
    elif app.patternMode:
        drawLabel("PATTERN MODE", 35, 30, size=16, font='montserrat', align='left')

def drawStationaryText(app):
    # board bottom left
    drawLabel("Return to Home : H", app.gridWin_l+15, app.gridWin_t+app.gridWin_h-15, size=12, fill='gray', font='montserrat', align='left')
    # board bottom right
    drawLabel("Clear All : R", app.gridWin_l+app.gridWin_w-15, app.gridWin_t + app.gridWin_h-30, size=12, fill='gray', font='montserrat', align='right')
    drawLabel("Rotate Board : → ", app.gridWin_l+app.gridWin_w-15, app.gridWin_t + app.gridWin_h-15, size=12, fill='gray', font='montserrat', align='right')
    # board top left
    # drawLabel("Rotate Tile : T", app.gridWin_l+15, app.gridWin_t +15, size=12, fill='gray', font='montserrat', align='left')
    # board top right
    drawLabel("Toggle Level Guard : L ", app.gridWin_l+app.gridWin_w-15, app.gridWin_t+15, size=12, fill='gray', font='montserrat', align='right')
    drawLabel("Move Level Guard : ↑ ↓", app.gridWin_l+app.gridWin_w-15, app.gridWin_t+30, size=12, fill='gray', font='montserrat', align='right')

def drawIsoGridTiles(app, level, b='gray', f=None, label=False, b_w=0.5, o=50):
    ''' Given level, draw isometric grid where each grid is tile dimension
        Default is background tile grid
        Label accounts for board rotation '''
    d = app.tileDim
    for r in range(app.rows):
        for c in range(app.cols):
            tx , ty = tileIndexToPixel(app, level, r, c)
            drawIsoRect(tx, ty, d, d, b=b, f=f, o=o, b_w=b_w)
            if label:
                if app.board_rotated == 0:
                    drawLabel(f"{level},{r},{c}", tx, ty+0.5*d, size=10, font='arial', 
                            fill="skyBlue", opacity=80) 
                if app.board_rotated == 1:
                    drawLabel(f"{level},{c},{app.rows-1-r}", tx, ty+0.5*d, size=10, font='arial', 
                            fill="skyBlue", opacity=80) 
                if app.board_rotated == 2:
                    drawLabel(f"{level},{app.rows-1-r},{app.cols-1-c}", tx, ty+0.5*d, size=10, font='arial', 
                            fill="skyBlue", opacity=80) 
                if app.board_rotated == 3:
                    drawLabel(f"{level},{app.cols-1-c},{r}", tx, ty+0.5*d, size=10, font='arial', 
                            fill="skyBlue", opacity=80) 

def drawIsoGridCubes(app, z, b='lightGray', f=None, label=False, b_w=0.2, o=100):
    ''' Given z, draw isometric grid where each grid is cube dimension
        Default is for current level'''
    d = app.cubeDim
    for x in range(app.rows*app.tileSize):
        for y in range(app.cols*app.tileSize):
            cx , cy = cubeIndexToPixel(app, z, x, y)
            drawIsoRect(cx, cy, d, d, b=b, f=f, o=o, b_w=b_w)

## Tile Functions ##
# 1. Tile set window
def drawTileOnCanvas(app, tile, px, py):
    '''Given Tile object, and pixel coordinate(center) of tile
        draw cubes according to tile map
        Used to draw tile set'''

    d = app.cubeDim

    levels, rows, cols = np.shape(tile.map)
    cubeInds = np.argwhere(tile.map == 1)
    for z,x,y in cubeInds:
        # cx, cy : pixel coordinate of cube origin (above top)
        cx = px + x*d - y*d 
        cy = py - z*d + x*d/2 + y*d/2

        # Draws only visible sides
        tt, tr, tb, tl = getCornerPointsIsoRect(cx, cy-d, d, d)
        bt, br, bb, bl = getCornerPointsIsoRect(cx, cy, d, d)

        if app.pathMode and ((z,y,x) == (1,1,1)): # in path finding mode, the center of tile is red
            if z==levels-1 or tile.map[z+1, x, y] != 1:
                drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='lightCoral') # draw top    
            if y==cols-1 or tile.map[z, x, y+1] != 1:
                drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='fireBrick') # draw left front
            if x==rows-1 or tile.map[z, x+1, y] != 1:
                drawPolygon(*tb, *tr, *br, *bb, border='black', borderWidth=0.3, fill='darkRed') # draw right front

        else:
            if z==levels-1 or tile.map[z+1, x, y] != 1:
                drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='white') # draw top    
            if y==cols-1 or tile.map[z, x, y+1] != 1:
                drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='gray') # draw left front
            if x==rows-1 or tile.map[z, x+1, y] != 1:
                drawPolygon(*tb, *tr, *br, *bb, border='white', borderWidth=0.3, fill='black') # draw right front

def drawTileSet(app):
    ''' Draws tile set on left side of page
    region for each tile
    3*3 place holders, margin is 0.25 * tileph_w / tileph_h, total 3.5 spaces
    tile-m-tile-m-tile
    m 
    tile-m-tile-m-tile
    ...
    '''
    tile_margin = 10
    l, t = app.tileWin_l+tile_margin, app.tileWin_t+tile_margin # left top of start drawing
    r, b = app.tileWin_l+app.tileWin_w-tile_margin, app.tileWin_t+app.tileWin_h-tile_margin # right, above
    w, h = r-l, b-t
    ph_w, ph_h = w/3.5, h/3.5

    # Draw each tile
    for i in range(len(app.tileSet.tiles)):
        # region for each tile
        tile = app.tileSet.tiles[i]
        row_i = i//3
        col_i = i%3
        px = l + col_i*1.25*ph_w+ph_w/2 # start + column index * (ph_w + 0.25*ph_(margin)) + ph_w/2
        py = t + row_i*1.25*ph_h+ph_h/2
        
        # place holder region
        drawPolygon(px-0.5*ph_w, py-0.5*ph_h, px+0.5*ph_w, py-0.5*ph_h, 
                    px+0.5*ph_w, py+0.5*ph_h, px-0.5*ph_w, py+0.5*ph_h, borderWidth=1,
                    fill=tile.background, border=None, opacity=20)
        # set tile object pixel coordinate    
        tile.px = px
        tile.py = py

        # draw guide boundary
        drawTileBound(app, tile)

        # draw tile
        drawTileOnCanvas(app, tile, px, py)


def drawTileBound(app, tile, b='lightSkyBlue', b_w=1, f=None, o=80, d=(1,3)):
    ''' Draw tile bounds
        Default is for dotted line around tile set
        Used for displaying legality when moving tile on board'''
    # from caresian rect > get corners of iso rectangles
    tt, tr, tb, tl = getCornerPointsIsoRect(tile.px, tile.py-app.tileDim, app.tileDim, app.tileDim)
    bt, br, bb, bl = getCornerPointsIsoRect(tile.px, tile.py, app.tileDim, app.tileDim)
    # Transparent
    drawPolygon(*tt, *tr, *tb, *tl, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # top
    drawPolygon(*tt, *tr, *tb, *tl, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # above
    drawPolygon(*tl, *bl, *bb, *tb, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # left front
    drawPolygon(*tb, *tr, *br, *bb, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # right front
    drawPolygon(*tl, *tt, *bt, *bl, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # left back
    drawPolygon(*tt, *tr, *br, *bt, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # right back

# 2. Tile 
def placeTileOnBoard(app, tile, l, r, c):
    ''' Given the board index l, r, c of tile,
        place tile on board by placing valid cube
        Accounts for board rotation status*
        '''
    # replace part of board map with tile map
    d = app.tileSize
    z, x, y = l*d, r*d, c*d
    app.board[z:z+d, x:x+d, y:y+d] = tile.map
    
    # place on board_tiles
    if app.board_rotated == 0:
        app.board_tiles[l,r,c] = tile
    elif app.board_rotated == 1:
        app.board_tiles[l, c, app.rows-1-r] = tile
    elif app.board_rotated == 2:
        app.board_tiles[l, app.rows-1-r, app.cols-1-c] = tile
    elif app.board_rotated == 3:
        app.board_tiles[l, app.cols-1-c, r] = tile 

    # set tile location value
    tile.onBoard = True
    tile.l, tile.r, tile.c = l, r, c
    tile.px, tile.py = -1, -1 # clearing values if any

    # in Pattern Mode reduce outcome board 
    app.outputBoard[(l,r,c)] = [tile]
    reduceNeighbors(app, l, r, c)

def removeTileFromBoard(app, tile, l, r, c):
    # revert app.board
    d = app.tileSize
    z, x, y = l*d, r*d, c*d
    app.board[z:z+d, x:x+d, y:y+d] = np.zeros((tile.size, tile.size, tile.size))

    # revert board_tiles
    if app.board_rotated == 0:
        app.board_tiles[l,r,c] = None
    elif app.board_rotated == 1:
        app.board_tiles[l, c, app.rows-1-r] = None
    elif app.board_rotated == 2:
        app.board_tiles[l, app.rows-1-r, app.cols-1-c] = None
    elif app.board_rotated == 3:
        app.board_tiles[l, app.cols-1-c, r] = None

def drawGrid(app):
    ''' Draws isometric grid and tiles placed on board.
        Draw only those faces from cube on board that are visable from view.
        (This reduces the number of shapes(faces) we need to draw)
        app.board = np.array (app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize)) 
        indices : levels -> z, rows -> x, cols -> y 
        '''

    # iso grid window border
    drawRect(app.gridWin_l, app.gridWin_t, app.gridWin_w, app.gridWin_h,
             border='lightgray', fill=None)
    
    for level in range(0, app.levels):
        drawIsoGridTiles(app, level, label=False) # level 1~tile grid: 

def drawLevelGuide(app):
    ''' draws level guide'''
    level = app.currentLevel
    if app.levelGuide:
        drawIsoGridTiles(app, level, label=True, o=100, f=None)
        drawIsoGridCubes(app, level*app.tileSize)
        drawPossibleTiles(app)

    
def drawBoard(app):
    # board size in units of cubes
    levels, rows, cols = app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize
    # i_w = 2*app.cubeDim
    # i_h = app.cubeDim
    d = app.cubeDim

    # go over cubes on board, check if face occluded, draw only when displayed
    cubeInds = np.argwhere(app.board == 1)
    for z,x,y in cubeInds:
        cx, cy = cubeIndexToPixel(app, z, x, y)
        bt, br, bb, bl = getCornerPointsIsoRect(cx, cy, d, d)
        tt, tr, tb, tl = getCornerPointsIsoRect(cx, cy-d, d, d)

        if z==levels-1 or app.board[z+1, x, y] != 1:
            drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='white') # draw top    
        if y==cols-1 or app.board[z, x, y+1] != 1:
            drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='gray') # draw left front
        if x==rows-1 or app.board[z, x+1, y] != 1:
            drawPolygon(*tb, *tr, *br, *bb, border='white', borderWidth=0.3, fill='black') # draw right front

def drawPossibleTiles(app):    
    # label possible tile for each tile on level guide
    for r in range(app.rows):
        for c in range(app.cols):
            tx,ty = tileIndexToPixel(app,app.currentLevel,r,c)
            drawLabel(f'{app.outputBoard[(app.currentLevel,r,c)]}', tx, ty+15, size=7, fill='gray')

def drawConstraints(app, tile): # NOT USED
    d = app.cubeDim
    tx, ty = tileIndexToPixel(app, tile.l, tile.r, tile.c)
    if tile.start != 0:
        z,x,y = app.tileSet.constraintDict[tile.start] # board location of tile start
        cx = tx + x*d - y*d 
        cy = ty + z*d + x*d/2 + y*d/2
        # bl = int(cx - d), int(cy + d)
        drawCircle(int(cx), int(cy), 3, fill='green') # start has green dot on above left corner
    if tile.end != 0:
        z,x,y = app.tileSet.constraintDict[tile.end]   # board location of tile end
        cx = tx + x*d - y*d 
        cy = ty + z*d + x*d/2 + y*d/2
        # tr = int(cx + d), int(cy - d)
        drawCircle(int(cx), int(cy), 3, fill='red') # end has red dot on top right corner

def drawMovingTile(app):
    ''' Draw moving tile when holding tile
        when on board, draw tile on board with snap and draw shadow
        when not on board, draw on mouse'''
    # if holding tile, draw current tile *above side left cube* on mouse position
    # (to visualize better!)
    if app.holdingTile:
        if not app.currentTile.onBoard: # not on board
            drawTileOnCanvas(app, app.currentTile, app.currentTile.px, app.currentTile.py)
        else:
            drawTileOnBoard(app, app.currentTile, app.currentTile.l, app.currentTile.r, app.currentTile.c)
    
def drawTileOnBoard(app, tile, l, r, c):
    '''Given Tile object, and board_tile index
        draw cubes according to tile map and bounding box
        Used to draw moving tile on board'''
    tx, ty = tileIndexToPixel(app, l, r, c)
    if isTileLegalOnBoard(app, tile, l, r, c):
        drawTileBound(app, app.currentTile, b=None, f='green', o=20)
    else:
        drawTileBound(app, app.currentTile, b=None, f='red', o=20)
    drawTileOnCanvas(app, tile, tx, ty)


## Path Finding ##
def isPath(app):
    ''' Checks if board currently has path
        If there exists path between START and END, returns cube unit path
        Else returns None
        User manually places tile on board and checks '''
    res = isPathHelper(app, app.START, 0, [app.START])
    if res != None:
        for cube in res:
            app.pathMap[cube] = 1
    return res

def isPathHelper(app, current, depth, path):
    '''if path is found, returns path (sequence of cube indices)'''
    # Terminate case : if current cube index is END
    if current == app.END:
        return path
    # Recursive case
    neighbors = getAllNeighborsCube(app, *current)# [under, above, left, right, top, bottom]
    # for all neighbors of current cube
    for n in neighbors:
        if n != tuple():
            if (n not in path) and (app.board[n] == 1): # if cube exists on board
                path.append(n) # add cube coordinate to path
                res = isPathHelper(app, n, depth+1, path)
                if res != None: return res
                else: 
                    path.remove(n)
    return None

def getAllNeighborsCube(app, z, x, y):
    ''' returns list of coordinates (z, x, y) of 
        under, above, left, right, top, bottom  cube neighbors
        blank tuple if wall'''
    boardZ, boardX, boardY = app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize
    under   = (z-1,x,y) if z>0 else tuple()
    above   = (z+1,x,y) if z<boardZ-1 else tuple()
    left    = (z,x-1,y) if x>0 else tuple()
    right   = (z,x+1,y) if x<boardX-1 else tuple()
    top     = (z,x,y-1) if y>0 else tuple()
    bottom  = (z,x,y+1) if y<boardY-1 else tuple()
    
    return [under, above, left, right, top, bottom]


## Pattern Generation ##
def patternGenerate(app):
    # start at 0,0,0
    start = (0,0,0)
    placeTileOnBoard(app, random.choice(app.tileSet.tiles), *start)
    path = [start] # stores l,c,r coordinates in order of selection
    patternGenerateHelper(app, path)

def patternGenerateHelper(app, path):
    pathSet = set(path)
    # base case : if all tiles have length one
    if len(path) == app.levels * app.rows * app.cols:
        app.foundPattern = True
        return path

    # for all neighboring tiles not in path
    current = path[-1]
    neighbors =  getAllNeighbors(app,*current)
    for next in neighbors:
        if next == () or (next in pathSet): continue
        # if any of neighbors empty, backtrack
        if len(app.outputBoard[next]) == 0:
            path.pop()
            return None

        for tile in app.outputBoard[next]:
            placeTileOnBoard(app, tile, *next)
            path.append(next)
            reduceNeighbors(app,*next)
            patternGenerateHelper(app, path)
    return None
        

def reduceNeighbors(app, l, r, c):
    # add neighbors to check queue
    # while queue is not empty,
        # pop from queue
        # reduce neighbors
        # if reduced, add to queue

    checkQueue = [(l,r,c)]
    while len(checkQueue) != 0:
        next = checkQueue.pop() # checking next neighbor
        reduced = reduceNeighborsHelper(app, *next)
        # if len(reduced) == 0:
        if reduced == None or len(reduced)==0:
            break
        checkQueue += reduced
    return 

def reduceNeighborsHelper(app, l, r, c):

    # for each neighboring direction
        # for each possible tile of neighbor
            # if there is tile in current possible that meets constraints, keep tile in neighbor
            # if no tile in current possible that meets constraints, delete from neighbor possible
    
    current_poss = app.outputBoard[l,r,c]
    
    # for all 6 neighboring directions
    under, above, left, right, top, bottom = getAllNeighbors(app,l,r,c) # coordinate of neighbors

    # retrieve list of possible tiles
    u_poss = app.outputBoard[under]  if len(under)!=0 else []
    a_poss = app.outputBoard[above]  if len(above)!=0 else []
    l_poss = app.outputBoard[left]   if len(left)!=0 else []
    r_poss = app.outputBoard[right]  if len(right)!=0 else []
    t_poss = app.outputBoard[top]    if len(top)!=0 else []
    b_poss = app.outputBoard[bottom] if len(bottom)!=0 else []
    
    
    # if not designated, or finished tile, can reduce
    if  not(\
        (len(u_poss)==0 or len(u_poss)==1) and \
        (len(a_poss)==0 or len(a_poss)==1) and \
        (len(l_poss)==0 or len(l_poss)==1) and \
        (len(r_poss)==0 or len(r_poss)==1) and \
        (len(t_poss)==0 or len(t_poss)==1) and \
        (len(b_poss)==0 or len(b_poss)==1)):
        
        # current possible tiles' compiled adjacencies
        u_comp, a_comp, l_comp, r_comp, t_comp, b_comp = set(), set(), set(), set(), set(), set()
        for tile in current_poss:
            u_comp.update(tile.adjUnder)
            a_comp.update(tile.adjAbove)
            l_comp.update(tile.adjLeft)
            r_comp.update(tile.adjRight)
            t_comp.update(tile.adjTop)
            b_comp.update(tile.adjBottom)
        
    
        # compare existing list and possible
        # leave only those that are possible in output board
        new_u_poss = set()
        new_a_poss = set()
        new_l_poss = set()
        new_r_poss = set()
        new_t_poss = set()
        new_b_poss = set()
        
        for u_t in u_poss:
            if u_t in u_comp: new_u_poss.add(u_t)
        for a_t in a_poss:
            if a_t in a_comp: new_a_poss.add(a_t)
        for l_t in l_poss:
            if l_t in l_comp: new_l_poss.add(l_t)
        for r_t in r_poss:
            if r_t in r_comp: new_r_poss.add(r_t)
        for t_t in t_poss:
            if t_t in t_comp: new_t_poss.add(t_t)
        for b_t in b_poss:
            if b_t in b_comp: new_b_poss.add(b_t)

        # return changed neighbors
        reducedNeighbors = []
        if under!=() and (len(app.outputBoard[under])  != len(new_u_poss)): reducedNeighbors.append(under)
        if above!=() and (len(app.outputBoard[above])  != len(new_a_poss)): reducedNeighbors.append(above)
        if left!=()  and (len(app.outputBoard[left])   != len(new_l_poss)): reducedNeighbors.append(left)
        if right!=() and (len(app.outputBoard[right])  != len(new_r_poss)): reducedNeighbors.append(right)
        if top!=()   and (len(app.outputBoard[top])    != len(new_t_poss)): reducedNeighbors.append(top)
        if bottom!=() and(len(app.outputBoard[bottom]) != len(new_b_poss)): reducedNeighbors.append(bottom)

        # update changed neighbors
        app.outputBoard[under]  = list(new_u_poss)
        app.outputBoard[above]  = list(new_a_poss)
        app.outputBoard[left]   = list(new_l_poss)
        app.outputBoard[right]  = list(new_r_poss)
        app.outputBoard[top]    = list(new_t_poss)
        app.outputBoard[bottom] = list(new_b_poss)

        return reducedNeighbors


def getAllNeighbors(app,l,r,c):
    ''' returns list of coordinate (l,r,c) of 
        under, above, left, right, top, bottom tile neighbors
        blank tuple if wall'''
    under   = (l-1,r,c) if l>0 else tuple()
    above   = (l+1, r, c) if l<app.levels-1 else tuple()
    left    = (l,r-1,c) if r>0 else tuple()
    right   = (l,r+1,c) if r<app.rows-1 else tuple()
    top     = (l,r,c-1) if c>0 else tuple()
    bottom  = (l,r,c+1) if c<app.cols-1 else tuple()
    
    return ([under, above, left, right, top, bottom])


def main():
    runApp(1200, 600)

main()