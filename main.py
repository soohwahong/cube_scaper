from cmu_cs3_graphics import *
import numpy as np
import settings 
import tile
import copy
from matplotlib import path

def onAppStart(app):

    app.setMaxShapeCount(100000)

    S = settings.getSettings()
    app.margin = S["margin"]

    # Tile & Cube
    app.tileSize = S["tileSize"] # num of cubes on one side of tile
    app.cubeDim = S["cubeDim"]   # pixel dim of one side of cube 
    app.tileDim = app.tileSize * app.cubeDim   # pixel dim of one side of tile
    app.tileSet = None 

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
    app.board = np.zeros((app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize)) # cube unit board
    app.board_tiles = np.zeros((app.levels, app.rows, app.cols)) # tile unit board

    # top pixel coordinate of background grid at level 0
    app.grid_ix, app.grid_iy = app.gridWin_l + app.gridWin_w/2, app.gridWin_t + app.tileDim * (app.levels + 2)

    # user action state
    app.holdingTile = False
    app.currentTile = None





########################TEST#################################
    # TEST : create tileset and draw

    three_tile_full = np.array([
        [[1,1,1],
         [1,1,1],
         [1,1,1]],
        [[1,1,1],
         [1,1,1],
         [1,1,1]],
        [[1,1,1],
         [1,1,1],
         [1,1,1]]
    ])
    
    three_tile = np.array([
        [[1,1,1],
         [1,0,0],
         [0,0,0]],
        [[0,0,0],
         [0,0,0],
         [0,0,0]],
        [[0,0,0],
         [0,0,0],
         [0,0,0]]
    ])
    r0 = tile.Tile("r0")
    r0.setMap(three_tile)
    # r1 = tile.Tile("r1")
    # r1.setMap(np.rot90(three_tile, 1, (2,1))) # counter clockwise
    # r2 = tile.Tile("r2")
    # r2.setMap(np.rot90(three_tile, 2, (2,1))) 
    # r3 = tile.Tile("r3")
    # r3.setMap(np.rot90(three_tile, 3, (2,1))) 
    # r4 = tile.Tile("r4")
    # r4.setMap(np.rot90(three_tile, 4, (2,1))) 

    # r1c = tile.Tile("r1c")
    # r1c.setMap(np.rot90(three_tile, 1, (1,2))) # clockwise

    # test_tileset = [test_tile] * 4 + [zero_tile] * 5
    test_tileset = [r0]
    app.tileSet = test_tileset


## Functions used on start

## Controllers

def onKeyPress(app, key):
    if key == 'q':
        return 42
    if app.holdingTile:
        if key == 'r':
            app.currentTile.rotate()

def onMousePress(app, mouseX, mouseY):
    if not app.holdingTile: # not holding tile
        # Case 1: Selecting tile anew to add to board
        select = isTileSelect(app, mouseX, mouseY)
        if select != None:
            app.holdingTile = True
            app.currentTile = select

    else: # holding tile
        select = isTileSelect(app, mouseX, mouseY)
        # Case 2: swap holding tile
        if select !=None:
            app.currentTile = select
        # Case 3: Place current tile on board if legal 
        else:
            if isTileLegalOnBoard(app, app.currentTile.l, app.currentTile.r, app.currentTile.c):
                # place tile on board
                placeTileOnBoard(app, app.currentTile, app.currentTile.l, app.currentTile.r, app.currentTile.c)
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
                # draw *bottom side left cube* of current tile on mouse position(to visualize better!)
            app.currentTile.px, app.currentTile.py = mouseX+app.tileDim, mouseY-app.tileDim//2


def isTileSelect(app, mouseX, mouseY):
    ''' Checks if click is on any tile in tile set window,
        and if it is, returns copy of clicked tile,
        otherwise return None'''
    for tile in app.tileSet:
        if ((tile.px-app.tileDim < mouseX < tile.px+app.tileDim)
            and (tile.py-app.tileDim < mouseY < tile.py+app.tileDim)):
            return copy.deepcopy(tile)
    return None

def inBoardRegion(app, mouseX, mouseY):
    ''' Checks if mouse is on isometric board window,
        and if it is, returns tile index (level, row, col),
        otherwise return None'''
    # for each index in board
    for l, r, c in (np.argwhere((app.board_tiles == 0) | (app.board_tiles == 1))):
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
def isTileLegalOnBoard(app, l, r, c):
    ''' Given tile index on board, 
        Returns boolean value of whether tile is legal 
        (there isn't any existing tile on board
         and meets adjacency constraints with 6 neighboring tiles '''
    # Checks existing
    if app.board_tiles[l,r,c] == 1: return False
    return True

    # Checks adjacency

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
    
    drawGrid(app)

    drawTileSet(app)

    drawBoard(app) 
    
    drawMovingTile(app)
        
    
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
    ''' Given pixel location ix,iy of bottom top point of cube,
        and dimension of cube, draw cube on canvas'''
    # get 6 points of cube by
    # level + 1 changes py -> py+h 
    # from caresian rect > get corners of iso rectangles
    tt, tr, tb, tl = getCornerPointsIsoRect(px, py-h, w, d)
    bt, br, bb, bl = getCornerPointsIsoRect(px, py, w, d)
    # Transparent
    # drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.5, opacity=30) # top
    # drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.5, fill=None) # bottom
    # drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.5, opacity=50) # left front
    # drawPolygon(*tb, *tr, *br, *bb, border='black', borderWidth=0.5, opacity=80) # right front
    # drawPolygon(*tl, *tt, *bt, *bl, border='grey', dashes=(2,4), borderWidth=0.5, fill=None) # left back
    # drawPolygon(*tt, *tr, *br, *bt, border='grey', dashes=(2,4), borderWidth=0.5, fill=None) # right back

    # Opaque
    drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='white') # top
    # drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill=None) # bottom
    drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='gray') # left front
    drawPolygon(*tb, *tr, *br, *bb, border='white', borderWidth=0.3, fill='black') # right front


def getCornerPointsIsoRect(ix, iy, w, h):
    ''' Given pixel coordinate of top point of iso rectangle cx, cy
        and width and height of cartesian rectangle
        return coordinates of four corners of isometric rectangle
        in order of top, right, bottom, left '''
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

def drawIsoGridTiles(app, level, b='skyBlue', f=None, label=False, b_w=0.5, o=100):
    ''' Given level, draw isometric grid where each grid is tile dimension'''
    d = app.tileDim
    for r in range(app.rows):
        for c in range(app.cols):
            tx , ty = tileIndexToPixel(app, level, r, c)
            drawIsoRect(tx, ty+level*d, d, d, b=b, f=f, o=o, b_w=b_w)
            if label:
                drawLabel(f"{level},{r},{c}", tx, ty+0.5*d, size=10, font='arial', 
                        fill="lightSkyBlue", opacity=80) 

def drawIsoGridCubes(app, z, b='lightSkyBlue', f=None, label=False, b_w=0.5, o=100):
    ''' Given z, draw isometric grid where each grid is cube dimension'''
    d = app.cubeDim
    for x in range(app.rows*app.tileSize):
        for y in range(app.cols*app.tileSize):
            cx , cy = cubeIndexToPixel(app, z, x, y)
            drawIsoRect(cx, cy+z*d, d, d, b=b, f=f, o=o, b_w=b_w)
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

    # Numpy version
    levels, rows, cols = np.shape(tile.map)
    cubeInds = np.argwhere(tile.map == 1)
    for z,x,y in cubeInds:
        # print(f'drawing tiles... {l} {r} {c} of tile map')
        # pixel coordinate of cube origin (bottom top)
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


def drawTileSet(app):
    ''' Draws tile set on left side of page'''
    # tile set window
    drawRect(app.tileWin_l, app.tileWin_t, app.tileWin_w, app.tileWin_h,
             border='darkSeaGreen', fill=None)

    # region for each tile
    tile_margin = 10
    l, t = app.tileWin_l+tile_margin, app.tileWin_t+tile_margin # left top of start drawing
    r, b = app.tileWin_l+app.tileWin_w-tile_margin, app.tileWin_t+app.tileWin_h-tile_margin # right, bottom
    w, h = r-l, b-t
    ph_w, ph_h = w/3.5, h/3.5
    # 3*3 place holders, margin is 0.25 * tileph_w / tileph_h, total 3.5 spaces
    # tile-m-tile-m-tile
    # m 
    # tile-m-tile-m-tile
    # ...

    # draw each tile
    for i in range(len(app.tileSet)):
        # region for each tile
        tile = app.tileSet[i]
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

def drawTileBound(app, tile, b='cyan', b_w=1, f=None, o=80, d=(1,2)):
    ''' Draw tile bounds
        Default is for dotted line around tile set
        Used for displaying legality when moving tile on board'''
    # from caresian rect > get corners of iso rectangles
    tt, tr, tb, tl = getCornerPointsIsoRect(tile.px, tile.py-app.tileDim, app.tileDim, app.tileDim)
    bt, br, bb, bl = getCornerPointsIsoRect(tile.px, tile.py, app.tileDim, app.tileDim)
    # Transparent
    drawPolygon(*tt, *tr, *tb, *tl, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # top
    drawPolygon(*tt, *tr, *tb, *tl, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # bottom
    drawPolygon(*tl, *bl, *bb, *tb, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # left front
    drawPolygon(*tb, *tr, *br, *bb, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # right front
    drawPolygon(*tl, *tt, *bt, *bl, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # left back
    drawPolygon(*tt, *tr, *br, *bt, border=b, borderWidth=b_w, fill=f, opacity=o, dashes=d) # right back

# 2. Tile 

def placeTileOnBoard(app, tile, l, r, c):
    ''' Given the board index l, r, c of tile,
        place tile on board by placing valid cube
        '''
    # replace part of board map with tile map
    # print(f'board shape is {app.board.shape} and tile shape is {tile.map.shape}')
    d = app.tileSize
    z, x, y = l*d, r*d, c*d
    app.board[z:z+d, x:x+d, y:y+d] = tile.map
    app.board_tiles[l,r,c] = 1
    # set tile location value
    tile.onBoard = True
    tile.l, tile.r, tile.c = l, r, c
    tile.px, tile.py = -1, -1 # clearing values if any

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
    drawIsoGridTiles(app, 0, label=True) # level 0 tile grid in default lines
    drawIsoGridCubes(app, 0, b='lightgray', b_w = 0.2)

    for level in range(1, app.levels):
        drawIsoGridTiles(app, level, label=True) # level 1~tile grid: 
    
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


def drawMovingTile(app):
    ''' Draw moving tile when holding tile
        when on board, draw tile on board with snap and draw shadow
        when not on board, draw on mouse'''
    # if holding tile, draw current tile *bottom side left cube* on mouse position
    # (to visualize better!)
    if app.holdingTile:
        if not app.currentTile.onBoard: # not on board
            drawTileOnCanvas(app, app.currentTile, app.currentTile.px, app.currentTile.py)
        else:
            drawTileOnBoard(app, app.currentTile, app.currentTile.l, app.currentTile.r, app.currentTile.c)
        

    # add rotation?

def drawTileOnBoard(app, tile, l, r, c):
    '''Given Tile object, and board_tile index
        draw cubes according to tile map and bounding box
        Used to draw moving tile on board'''
    tx, ty = tileIndexToPixel(app, l, r, c)
    if isTileLegalOnBoard(app, l, r, c):
        drawTileBound(app, app.currentTile, b=None, f='green', o=20)
    else:
        drawTileBound(app, app.currentTile, b=None, f='red', o=20)
    drawTileOnCanvas(app, tile, tx, ty)

def main():
    runApp(1200, 600)

main()