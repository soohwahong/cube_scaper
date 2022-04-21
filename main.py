from operator import truediv
from cmu_cs3_graphics import *
import numpy as np
import settings 
from tile import *
import copy
from matplotlib import path
from tileSetA import *
from wfc import *

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
    # app.setMaxShapeCount(100000)

    S = settings.getSettings()
    app.margin = S["margin"]

    # Tile & Cube
    app.tileSize = S["tileSize"] # num of cubes on one side of tile
    app.cubeDim = S["cubeDim"]   # pixel dim of one side of cube 
    app.tileDim = app.tileSize * app.cubeDim   # pixel dim of one side of tile
    app.tileSet = tileSetA

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
    # app.board_tiles = np.zeros((app.levels, app.rows, app.cols)) # tile unit board
    # tile unit board : stores tile objects
    app.board_tiles = np.empty((app.levels, app.rows, app.cols), dtype=object)
    # records number of rotations counter clockwise of board. 
    # 0 is default 0~3
    app.board_rotated = 0
    
    #top pixel coordinate of background grid at level 0
    app.grid_ix, app.grid_iy = app.gridWin_l + app.gridWin_w/2, app.gridWin_t + app.tileDim * (app.levels + 2)

    # user action state
    app.holdingTile = False
    app.currentTile = None

    # drawing reference
    app.currentLevel = 0

    # Path Finding
    app.pathFinding = False
    app.settingHome = False
    app.settingDest = False
    app.home = None
    app.dest = None

    app.running = True

## TODO : Set home and goal tile on board ##

## Functions used on start

## Controllers

def onKeyPress(app, key):
    if key == 'q':
        return 42
    
    # Rotate Holding tile
    if app.holdingTile:
        if key == 'r':
            app.currentTile.rotate()
            # print(f'{app.currentTile.name} is rotated {app.currentTile.rotated} \
            #     and start, end is {app.currentTile.start, app.currentTile.end}')

    # Control Level guide
    if (key == 'up') and (app.currentLevel<app.levels-1):
        app.currentLevel += 1
    if (key == 'down') and (app.currentLevel>0):
        app.currentLevel -= 1

    # Rotate board
    if (key == 'right'):
        rotateBoard(app)

    # Setting home
    if (key == 'h'):
        app.settingHome = True
        app.settingDest = False
    
    if key == 'd':
        app.settingDest = True
        app.settingHome = False

    if key == 'p':
        # pathFind(app)
        app.pathFinding = True
    
    if key == 'q':
        app.running = False
        

def rotateBoard(app):
    ''' On right press, rotate the board
        '''
    app.board = np.rot90(app.board, 1, (1,2))
    app.board_rotated = (app.board_rotated+1)%4
    # print(f'at rotation {app.board_rotated}, board is \n{app.board}')
    

def onMousePress(app, mouseX, mouseY):
    if not app.holdingTile: # not holding tile
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
        # Case 3: Place current tile on board if legal 
        else:
            if isTileLegalOnBoard(app, app.currentTile, app.currentTile.l, app.currentTile.r, app.currentTile.c):
                # place tile on board
                placeTileOnBoard(app, app.currentTile, app.currentTile.l, app.currentTile.r, app.currentTile.c)
                print(f'current board = \n{app.board_tiles}')
                
                # if setting home, placed tile is home
                if app.settingHome:
                    app.home = copy.deepcopy(app.currentTile)
                if app.settingDest:
                    app.dest = copy.deepcopy(app.currentTile)
                app.settingHome = False
                app.settingDest = False

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
            return copy.deepcopy(tile)
    return None

def inBoardRegion(app, mouseX, mouseY):
    ''' Checks if mouse is on isometric board window,
        and if it is, returns tile index (level, row, col),
        otherwise return None'''
    # for each index in board
    # for l, r, c in (np.argwhere((app.board_tiles == 0) | (app.board_tiles == 1))):
    for l, r, c in np.argwhere(app.board_tiles!=0): # get all indices of board tile
        # get four corners pixel coordinates in order t, r, b, l
        d = app.tileDim
        tx ,ty = tileIndexToPixel(app,l,r,c)
        rx, ry = tx+d, ty-0.5*d
        bx, by = tx, ty+d
        lx, ly = tx-d, ty-0.5*d
        
        xv = np.array([tx, rx, bx, lx])
        yv = np.array([ty, ry, by, ly])
        if inPolygon(np.array([mouseX]), np.array([mouseY]), xv, yv):
            return l, r, c

#################### TODO : checks adjacency ####################
def isTileLegalOnBoard(app, tile, l, r, c):
    ''' Given tile and tile index on board, 
        Returns boolean value of whether tile is legal 
        (there isn't any existing tile on board
         and meets adjacency constraints with neighboring tiles (3 previous, 3 next tiles)'''
    # Checks existing
    if app.board_tiles[l,r,c] != None: return False

    # Checks adjacency
    if checkPreviousTile(app, tile,l,r,c) == False : return False
    # if checkNextTile(app, tile,l,r,c) == False : return False

    return True

# def checkNextTile(app, tile,l,r,c):
#     ''' Checks 3 neighbors of end cube of current tile, 
#         if all 3 neighbors are full, 
#         at least one next.start should meet current.end''' 
#     return 42

def checkPreviousTile(app, tile,l,r,c):
    '''Checks 3 neighbors of start cube of current tile,
       if previous tile exists, previous.end must meet current.start'''
    # print(f'Checking previous tile for {tile.name}, {l,r,c}, {tile.start, tile.end}')
    # start is at above side cube
    if tile.start == 4:
        if c<app.cols-1 and (app.board_tiles[l,r,c+1] != None) and (app.board_tiles[l,r,c+1].end != 1): return False # column direction
        if r>=1 and (app.board_tiles[l,r-1,c] != None) and (app.board_tiles[l,r-1,c].end != 3): return False # row direction
        if l>=1 and (app.board_tiles[l-1,r,c] != None) and (app.board_tiles[l-1,r,c].end != 8): return False # level direction
    elif tile.start == 3:
        if c<app.cols-1 and (app.board_tiles[l,r,c+1] != None) and (app.board_tiles[l,r,c+1].end != 2): return False # column direction
        if r<app.rows-1 and (app.board_tiles[l,r+1,c] != None) and (app.board_tiles[l,r+1,c].end != 4): return False # row direction
        if l>=1 and (app.board_tiles[l-1,r,c] != None) and (app.board_tiles[l-1,r,c].end != 7): return False # level direction
    elif tile.start == 2:
        if c>=1 and (app.board_tiles[l,r,c-1] != None) and (app.board_tiles[l,r,c-1].end != 3): return False # column direction
        if r<app.rows-1 and (app.board_tiles[l,r+1,c] != None) and (app.board_tiles[l,r+1,c].end != 1): return False # row direction
        if l>=1 and (app.board_tiles[l-1,r,c] != None) and (app.board_tiles[l-1,r,c].end != 6): return False # level direction
    elif tile.start == 1:
        if c>=1 and (app.board_tiles[l,r,c-1] != None) and (app.board_tiles[l,r,c-1].end != 4): return False # column direction
        if r>=1 and (app.board_tiles[l,r-1,c] != None) and (app.board_tiles[l,r-1,c].end != 2): return False # row direction
        if l>=1 and (app.board_tiles[l-1,r,c] != None) and (app.board_tiles[l-1,r,c].end != 5): return False # level direction
    # start is at top cube
    elif tile.start == 8:
        if c<app.cols-1 and (app.board_tiles[l,r,c+1] != None) and (app.board_tiles[l,r,c+1].end != 5): return False # column direction
        if r>=1 and (app.board_tiles[l,r-1,c] != None) and (app.board_tiles[l,r-1,c].end != 7): return False # row direction
        if l<app.levels and (app.board_tiles[l+1,r,c] != None) and (app.board_tiles[l+1,r,c].end != 4): return False # level direction
    elif tile.start == 7:
        if c<app.cols-1 and (app.board_tiles[l,r,c+1] != None) and (app.board_tiles[l,r,c+1].end != 6): return False # column direction
        if r<app.rows-1 and (app.board_tiles[l,r+1,c] != None) and (app.board_tiles[l,r+1,c].end != 8): return False # row direction
        if l<app.levels and (app.board_tiles[l+1,r,c] != None) and (app.board_tiles[l+1,r,c].end != 3): return False # level direction
    elif tile.start == 6:
        if c>=1 and (app.board_tiles[l,r,c-1] != None) and (app.board_tiles[l,r,c-1].end != 7): return False # column direction
        if r<app.rows-1 and (app.board_tiles[l,r+1,c] != None) and (app.board_tiles[l,r+1,c].end != 5): return False # row direction
        if l<app.levels and (app.board_tiles[l+1,r,c] != None) and (app.board_tiles[l+1,r,c].end != 2): return False # level direction
    elif tile.start == 5:
        if c>=1 and (app.board_tiles[l,r,c-1] != None) and (app.board_tiles[l,r,c-1].end != 8): return False # column direction
        if r>=1 and (app.board_tiles[l,r-1,c] != None) and (app.board_tiles[l,r-1,c].end != 6): return False # row direction
        if l<app.levels and (app.board_tiles[l+1,r,c] != None) and (app.board_tiles[l+1,r,c].end != 1): return False # level direction
    
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

    
## Draw
def redrawAll(app):
    
    drawTileSet(app)
    drawGrid(app)
    if app.running:
        if app.pathFinding:
            pathFind(app)
        drawBoard(app) 
        drawLevelGrid(app)
        drawMovingTile(app)
        drawStatusBar(app)
        

def drawStatusBar(app):
    ''' Writes messages and status of game on top of page'''
    label = "Hello"
    if app.settingHome:
        label = "Pick a Home tile, rotate and drop it on the Board"
    if app.settingDest:
        label = "Pick a Destination tile, rotate and drop it on the Board"
    
    drawLabel(label, 50, 25, size=16, font='montserrat', align='left')

## Isometric Functions ##
def cartToIso(x, y):
    isoX = x - y
    isoY = (x+y)*0.5
    return int(isoX), int(isoY)
    # return isoX, isoY
    
def isoToCart(ix, iy):
    cx = (ix + 2*iy)/2
    cy = (-ix + 2*iy)/2
    # return int(cx), int(cy)
    return cx, cy

def tileIndexToPixel(app, l, r, c):
    '''Given 3d board coordinate of tile unit l, c, r,
    Return pixel coordinate of origin point(center) tx, ty
    isometric width is 2*tileDim and height is 1*tileDim
    Make sure that pixel value is integer!
    '''
    d = app.tileDim
    tx = app.grid_ix + r*d - c*d 
    ty = app.grid_iy + r*0.5*d + c*0.5*d - l*d
    # return int(tx), int(ty)
    return tx, ty

def cubeIndexToPixel(app, z, x, y):
    '''Given 3d board coordinate of cube unit z, y, x
    Return pixel coordinate of origin point(center) cx, cy
    isometric width is 2*cubeDim and height is 1*cubeDim
    Make sure that pixel value is integer!
    '''
    d = app.cubeDim
    cx = app.grid_ix + x*d - y*d 
    cy = app.grid_iy + x*0.5*d + y*0.5*d - z*d
    # return int(cx), int(cy)
    return cx, cy

      
def drawIsoCube(px, py, w, d, h): ###### NO USE
    ''' Given pixel location ix,iy of above top point of cube,
        and dimension of cube, draw cube on canvas'''
    # get 6 points of cube by
    # level + 1 changes py -> py+h 
    # from caresian rect > get corners of iso rectangles
    tt, tr, tb, tl = getCornerPointsIsoRect(px, py-h, w, d)
    bt, br, bb, bl = getCornerPointsIsoRect(px, py, w, d)
    # Transparent
    # drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.5, opacity=30) # top
    # drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.5, fill=None) # above
    # drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.5, opacity=50) # left front
    # drawPolygon(*tb, *tr, *br, *bb, border='black', borderWidth=0.5, opacity=80) # right front
    # drawPolygon(*tl, *tt, *bt, *bl, border='grey', dashes=(2,4), borderWidth=0.5, fill=None) # left back
    # drawPolygon(*tt, *tr, *br, *bt, border='grey', dashes=(2,4), borderWidth=0.5, fill=None) # right back

    # Opaque
    drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='white') # top
    # drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill=None) # above
    drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='gray') # left front
    drawPolygon(*tb, *tr, *br, *bb, border='white', borderWidth=0.3, fill='black') # right front


def getCornerPointsIsoRect(ix, iy, w, h):
    ''' Given pixel coordinate of top point of iso rectangle cx, cy
        and width and height of cartesian rectangle
        return coordinates of four corners of isometric rectangle
        in order of top, right, above, left '''
    # # points in clockwise order
    # 1 2
    # 4 3
    #   1
    # 4   2
    #   3

    # cx , cy is top left corner of cartesian rectangle
    cx, cy = isoToCart(ix, iy)
    
    tl_x, tl_y = cx  , cy
    tr_x, tr_y = cx+w, cy
    br_x, br_y = cx+w, cy+h
    bl_x, bl_y = cx  , cy+h
    
    iso_t_x, iso_t_y = cartToIso(tl_x, tl_y)
    iso_r_x, iso_r_y = cartToIso(tr_x, tr_y)
    iso_b_x, iso_b_y = cartToIso(br_x, br_y)
    iso_l_x, iso_l_y = cartToIso(bl_x, bl_y)
    
    # drawRect(tl_x, tl_y, w, h, opacity=20)
    return [(iso_t_x, iso_t_y), (iso_r_x, iso_r_y), (iso_b_x, iso_b_y), (iso_l_x, iso_l_y)]

def drawIsoRect(ix, iy, w, h, b='black', f=None, o=100, b_w=0.5):
    ''' Given '''
    # ix, iy is top point of isometric rect
    cx, cy = isoToCart(ix, iy)
    
    # # points in clockwise order
    # 1 2
    # 4 3
    #   1
    # 4   2
    #   3
    tl_x, tl_y = cx  , cy
    tr_x, tr_y = cx+w, cy
    br_x, br_y = cx+w, cy+h
    bl_x, bl_y = cx  , cy+h
    
    
    iso_t_x, iso_t_y = cartToIso(tl_x, tl_y)
    iso_r_x, iso_r_y = cartToIso(tr_x, tr_y)
    iso_b_x, iso_b_y = cartToIso(br_x, br_y)
    iso_l_x, iso_l_y = cartToIso(bl_x, bl_y)
    
    # drawRect(tl_x, tl_y, w, h, opacity=20)
    drawPolygon(iso_t_x, iso_t_y, iso_r_x, iso_r_y, iso_b_x, iso_b_y, 
                iso_l_x, iso_l_y, border=b ,borderWidth=b_w, opacity=o, 
                fill=f)  

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
            # if label:
            #     drawLabel(f"{r},{c}", app.grid_ix, app.grid_iy+0.5*d, size=10, font='arial', 
            #             fill="blue", opacity=80) 


def drawCartGrid(cx, cy, rows, cols, d): ####### NO USE
    for r in range(rows):
        for c in range(cols):
            drawRect(cx+r*d,cy+c*d, d, d, border='black', borderWidth=1, fill=None, opacity=40)
            drawLabel(f"{r},{c}", cx+r*d +0.5*d, cy+c*d + 0.5*d, size=10, font='arial', 
                      fill="orange", opacity=80)
                      
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
        # print(f'drawing tiles... {l} {r} {c} of tile map')
        # pixel coordinate of cube origin (above top)
        cx = px + x*d - y*d 
        cy = py - z*d + x*d/2 + y*d/2

        ## integrating drawIsoCube(t_ix, t_iy, d, d, d) so that draw less shapes
        tt, tr, tb, tl = getCornerPointsIsoRect(cx, cy-d, d, d)
        bt, br, bb, bl = getCornerPointsIsoRect(cx, cy, d, d)

        if z==levels-1 or tile.map[z+1, x, y] != 1:
            drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='white') # draw top    
        if y==cols-1 or tile.map[z, x, y+1] != 1:
            drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='gray') # draw left front
        if x==rows-1 or tile.map[z, x+1, y] != 1:
            drawPolygon(*tb, *tr, *br, *bb, border='white', borderWidth=0.3, fill='black') # draw right front

        # indicate start and end constraint
        # print(f'{tile.start, tile.end}')
        startCube = app.tileSet.constraintDict[tile.start]
        endCube = app.tileSet.constraintDict[tile.end]
        # print(f'{tile.name, startCube, endCube}')
        if tile.start != 0:
            if (z,x,y) == startCube:
                drawCircle(int(cx),int(cy), 3, fill='green') # start has green dot on above left corner
        if tile.end != 0:
            if (z,x,y) == endCube:
                drawCircle(int(cx),int(cy), 3, fill='red') # end has red dot on top right corner

def drawTileSet(app):
    ''' Draws tile set on left side of page'''
    # tile set window
    drawRect(app.tileWin_l, app.tileWin_t, app.tileWin_w, app.tileWin_h,
             border='darkSeaGreen', fill=None)

    # region for each tile
    tile_margin = 10
    l, t = app.tileWin_l+tile_margin, app.tileWin_t+tile_margin # left top of start drawing
    r, b = app.tileWin_l+app.tileWin_w-tile_margin, app.tileWin_t+app.tileWin_h-tile_margin # right, above
    w, h = r-l, b-t
    ph_w, ph_h = w/3.5, h/3.5
    # 3*3 place holders, margin is 0.25 * tileph_w / tileph_h, total 3.5 spaces
    # tile-m-tile-m-tile
    # m 
    # tile-m-tile-m-tile
    # ...

    # draw each tile
    for i in range(len(app.tileSet.tiles)):
        # region for each tile
        tile = app.tileSet.tiles[i]
        row_i = i//3
        col_i = i%3
        px = l + col_i*1.25*ph_w+ph_w/2 # start + column index * (ph_w + 0.25*ph_(margin)) + ph_w/2
        py = t + row_i*1.25*ph_h+ph_h/2

        # set tile object pixel coordinate    
        tile.px = px
        tile.py = py

        # draw guide boundary
        drawTileBound(app, tile)

        # draw tile
        drawTileOnCanvas(app, tile, px, py)

        # place holder region
        drawPolygon(px-0.5*ph_w, py-0.5*ph_h, px+0.5*ph_w, py-0.5*ph_h, 
                    px+0.5*ph_w, py+0.5*ph_h, px-0.5*ph_w, py+0.5*ph_h, borderWidth=1,
                    fill=None, border='yellowGreen', dashes=True)

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
    # print(f'board shape is {app.board.shape} and tile shape is {tile.map.shape}')
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

    # revert tile assets
    # set tile location value
    # tile.onBoard = False
    # tile.l, tile.r, tile.c = -1, -1, -1
    # tile.px, tile.py = -1, -1 # clearing values if any
    
def drawGrid(app):
    ''' Draws isometric grid and tiles placed on board.
        Draw only those faces from cube on board that are visable from view.
        (This reduces the number of shapes(faces) we need to draw)
        app.board = np.array (app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize)) 
        indices : levels -> z, rows -> x, cols -> y 
        '''

    # iso grid window border
    drawRect(app.gridWin_l, app.gridWin_t, app.gridWin_w, app.gridWin_h,
             border='skyBlue', fill=None)
    
    # top pixel coordinates of grid
    # grid_ix, grid_iy = app.gridWin_l + app.gridWin_w/2, app.gridWin_t + app.tileDim * (app.levels + 2)
    
    # background iso grid
    # drawIsoGridTiles(app, 0, label=True) # level 0 tile grid in default lines
    # drawIsoGridCubes(app, 0, b='lightgray', b_w = 0.2)

    for level in range(0, app.levels):
        drawIsoGridTiles(app, level, label=False) # level 1~tile grid: 

def drawLevelGrid(app):
    level = app.currentLevel
    # drawIsoGridTiles(app, level, label=True, o=30, f='lightSkyBlue')
    drawIsoGridTiles(app, level, label=True, o=100, f=None)
    drawIsoGridCubes(app, level*app.tileSize)

    
def drawBoard(app):
    # board size in units of cubes
    levels, rows, cols = app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize
    # i_w = 2*app.cubeDim
    # i_h = app.cubeDim
    d = app.cubeDim

    # go over cubes on board, check if face occluded, draw only when displayed
    
    # go over cubes on board before current layer
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

    # go over tiles on board, draw start and end
    tileInds = np.argwhere(app.board_tiles!=None)
    for l,r,c in tileInds:
        tile = app.board_tiles[l,r,c]
        drawConstraints(app, tile)

def drawConstraints(app, tile):
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
def pathFind(app):
    '''Given home tile and goal tile, 
       create sequence of tiles starting from home to goal'''
    return pathFindHelper(app, app.home, 0)

def pathFindHelper(app, current, depth):
    ''' Given current tile, search neighbors for valid next tile 
        Recursively search next tile
        Backtrack if no possible next neighbor'''
    # for 3 neighbors of current, if (next, rotate) meets, place
    # if none of neighbors can meet, backtrack
    # goal state: next tile is goal and meets
    print(f'\nFinding Path at depth {depth}..')
    print(f'current = {current, current.l, current.r, current.c}')
    nextTiles = getNextNeighbors(app, current) # list of 3 neighboring tile coordinates of current.end on board
    print(f'next tiles = {nextTiles}')
    
    # 
    if len(nextTiles) == 0: # back track
        print('**We are returning none because no more neighbors')
        removeTileFromBoard(app, current, current.l, current.r, current.c)
        return None
    
    for nl, nr, nc in nextTiles: # for each neighboring location
        if (nl, nr, nc) == (app.dest.l, app.dest.r, app.dest.c): # goal state
            if TilesMeet(current, app.dest):
                print("Reached Destination!") 
                # app.pathFinding = False # cannot change app.pathFinding
                return app.dest
            else: 
                print('**We are returning none because destination was not met**\n')
                removeTileFromBoard(app, current, current.l, current.r, current.c)
                return None
        
        for t in app.tileSet.tiles: # for each tile type in tile set
            next = copy.deepcopy(t)
            next.l, next.r, next.c = nl,nr,nc
            for r in range(4): # for each rotation
                next.rotate()
                if TilesMeet(current, next): # if next tile meets with current, place next tile
                    print("tiles Meet!")
                    print(f'Placing {next, next.l, next.r, next.c}')
                    placeTileOnBoard(app, next, next.l, next.r, next.c)
                    # Draw updated Tile
                    drawBoard(app)
                    drawLevelGrid(app)
                    drawMovingTile(app)
                    drawStatusBar(app)

                    print(f'Next before recursion step is {next.name}, {next.l,next.r,next.c}')
                    res = pathFindHelper(app, next, depth+1)
                    print(f'Next after recursion step is {next.name}, {next.l,next.r,next.c}')
                    if res == app.dest: return app.dest
                    elif res == None: 
                        print(f'Removing {next, next.l, next.r, next.c}')
                        removeTileFromBoard(app, next, next.l, next.r, next.c) # remove tile from board
        return None


def getNextNeighbors(app, tile):
    '''Given tile, 
       Return list of l,c,r coordinates of max 3 neighboring tiles of tile.end'''
    res = []
    back  = (tile.l, tile.r, tile.c-1)
    front = (tile.l, tile.r, tile.c+1)
    left  = (tile.l, tile.r-1, tile.c)
    right = (tile.l, tile.r+1, tile.c)
    under = (tile.l-1, tile.r, tile.c)
    above = (tile.l+1, tile.r, tile.c)

    if tile.end == 1: # back, left, under
        if locationValid(app,*back): res.append(back)
        if locationValid(app,*left): res.append(left)
        if locationValid(app,*under): res.append(under)
    if tile.end == 2: # back, right, under
        if locationValid(app,*back): res.append(back)
        if locationValid(app,*right): res.append(right)
        if locationValid(app,*under): res.append(under)
    if tile.end == 3: # front, right, under
        if locationValid(app,*front): res.append(front)
        if locationValid(app,*right): res.append(right)
        if locationValid(app,*under): res.append(under)
    if tile.end == 4: # front, left, under
        if locationValid(app,*front): res.append(front)
        if locationValid(app,*left): res.append(left)
        if locationValid(app,*under): res.append(under)
    if tile.end == 5: # back, left, above
        if locationValid(app,*back): res.append(back)
        if locationValid(app,*left): res.append(left)
        if locationValid(app,*above): res.append(above)
    if tile.end == 6: # back, right, above
        if locationValid(app,*back): res.append(back)
        if locationValid(app,*right): res.append(right)
        if locationValid(app,*above): res.append(above)
    if tile.end == 7: # front, right, above
        if locationValid(app,*front): res.append(front)
        if locationValid(app,*right): res.append(right)
        if locationValid(app,*above): res.append(above)
    if tile.end == 8: # front, left, above
        if locationValid(app,*front): res.append(front)
        if locationValid(app,*left): res.append(left)
        if locationValid(app,*above): res.append(above)
    
    return res

def locationValid(app,l,r,c):
    ''' Helper function for getNextNeighbor.
        Check if all values of l,r,c are within board'''
    if l<0 or app.levels<=l: return False
    if r<0 or app.rows<=r: return False
    if c<0 or app.cols<=c: return False
    return True
    
        
def TilesMeet(current, compare):
    '''Given two tiles current and compare, 
       check if current.end meets with compare.start'''
    print(f'Checking Adjacency ... \
        \n--Current:{current.name}, {current.l,current.r,current.c} & \
        \n--Compare:{compare.name}, {compare.l,compare.r,compare.c}')
    
    # two tiles have to be neighboring
    if abs(current.l-compare.l) + abs(current.r-compare.r) + abs(current.c-compare.c) != 1: 
        print("Two tiles do not meet!")
        return False
    if current.l - compare.l == 1: # current on top of compare
        if current.end > 4: 
            print('above')
            return False # current end on top side!
        if compare.start - current.end != 4: 
            print("above diff")
            return False
    if current.l - compare.l == -1: # current under compare
        if current.end < 5: 
            print("under")
            return False # current end on above side!
        if current.end - compare.start != 3: 
            print("under diff")
            return False
    
    if current.r - compare.r == 1: # current on right side of compare
        if current.end not in [1,4,5,8]: 
            print("right")
            return False # current end on left side
        if current.end in [1,5]:
            if compare.start != current.end+1: 
                print("right diff1")
                return False
        if current.end in [4,8]:
            if compare.start != current.end-1: 
                print("right diff2")
                return False
    
    if current.r - compare.r == -1: # current on left side of compare
        if current.end not in [2,3,6,7]: 
            print("left")
            return False # current end on right side!
        if current.end in [3,7]:
            if compare.start != current.end+1:
                print("left diff1")
                return False
        if current.end in [2,6]:
            if compare.start != current.end-1: 
                print("left diff2")
                return False
        
    if current.c - compare.c == 1: # current on front side of compare
        if current.end not in [1,2,5,6]: 
            print("front")
            return False # current end on left side!
        if current.end in [2,6]:
            if compare.start != current.end+1: 
                print("front diff1")
                return False
        if current.end in [1,5]:
            if compare.start != current.end+3: 
                print("front diff2")
                return False
    if current.c - compare.c == -1: # current on back side of compare
        if current.end not in [3,4,7,8]: 
            print("back")
            return False # current end on right side
        if current.end in [3,7]:
            if compare.start != current.end-1: 
                print("back diff1")
                return False
        if current.end in [4,8]:
            if compare.start != current.end-3: 
                print("back diff2")
                return False
    return True
                

def main():
    runApp(1200, 600)

main()