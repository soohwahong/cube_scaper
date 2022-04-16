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

    app.drawnTiles = []




########################TEST#################################
    # TEST : create tileset and draw
    test_tile = tile.Tile("test_tile")
    zero_tile = tile.Tile("zero_tile")
    five_tile = np.array([
        [[1,1,1,1,1],
         [1,1,1,1,1],
         [0,0,1,1,0],
         [0,0,1,1,0],
         [0,0,1,1,0]],
        [[1,1,1,1,1],
         [1,1,1,1,1],
         [0,0,1,1,0],
         [0,0,1,1,0],
         [0,0,1,1,0]],
        [[1,1,1,1,1],
         [1,1,1,1,1],
         [0,0,1,1,0],
         [0,0,1,1,0],
         [0,0,1,1,0]],
        [[1,1,1,1,1],
         [1,1,1,1,1],
         [0,0,1,1,0],
         [0,0,1,1,0],
         [0,0,1,1,0]],
        [[1,0,0,0,1],
         [1,0,0,0,1],
         [0,1,0,1,0],
         [0,1,0,1,0],
         [0,1,0,1,0]]
      ])

    three_tile = np.array([
        [[1,1,1],
         [1,0,0],
         [1,0,0]],
        [[0,0,0],
         [0,0,0],
         [0,0,0]],
        [[0,0,0],
         [0,0,0],
         [0,0,0]]
    ])
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
    
    test_tile.setMap(three_tile)

    # test_tileset = [test_tile] * 4 + [zero_tile] * 5
    test_tileset = [test_tile]
    app.tileSet = test_tileset


## Functions used on start

## Controllers

def onKeyPress(app, key):
    if key == 'q':
        return 42

def onMousePress(app, mouseX, mouseY):
    # Case 1: Selecting tile to add to board
    select = isTileSetRegion(app, mouseX, mouseY)
    if select != None:
        if (not app.holdingTile): # selecting tile anew
            app.holdingTile = True
        # setting current tile to select tile
        app.currentTile = select

    # Case 2:
    # place on board if legal place (including adjacency constraints)
    # if
    




def onMouseMove(app, mouseX, mouseY):

    if app.holdingTile:
        # if in board region, snap to board 
        if (inBoardRegion(app, mouseX, mouseY)!=None):
            # set tile attributes
                # set on board to true
            app.currentTile.onBoard = True
                # set tile location to snap to board
            l, c, r = inBoardRegion(app, mouseX, mouseY) # board coordinate of tile
            app.currentTile.l, app.currentTile.c, app.currentTile.r = l, c, r
            app.currentTile.px, app.currentTile.py = tileIndexToPixel(app,l,c,r)
            
            # if tile legal on board(no tile & satisfies adjacency rule), show green shadow, if not show red
                # first clear board color
            app.board_green = np.zeros((app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize))
            app.board_red = np.zeros((app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize))
            if isTileLegalOnBoard(app, l, c, r):
                size = app.currentTile.size
                app.board_green[l:l+size, c:c+size, r:r+size] = app.currentTile.map
            else:
                app.board_red[l:l+size, c:c+size, r:r+size] = app.currentTile.map
        # if not in board region, draw on mouse
        else:
            # set tile attributes
                # set on board to true
            app.currentTile.onBoard = False
            app.currentTile.l, app.currentTile.c, app.currentTile.r = -1, -1, -1
                # set tile location to mouse
                # draw *bottom side left cube* of current tile on mouse position(to visualize better!)
            app.currentTile.px, app.currentTile.py = mouseX+app.tileDim, mouseY-app.tileDim//2


        


def isTileSetRegion(app, mouseX, mouseY):
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
        and if it is, returns tile index (level, col, row),
        otherwise return None'''
    # for each index in board
    for l, c, r in (np.argwhere((app.board_tiles == 0) | (app.board_tiles == 1))):
        # get four corners pixel coordinates in order t, r, b, l
        d = app.tileDim
        tx ,ty = tileIndexToPixel(app,l,c,r)
        rx, ry = tx+d, ty-0.5*d
        bx, by = tx, ty+d
        lx, ly = tx-d, ty-0.5*d
        
        xv = np.array([tx, rx, bx, lx])
        yv = np.array([ty, ry, by, ly])
        if inPolygon(np.array([mouseX]), np.array([mouseY]), xv, yv):
            print("Mouse is in board region!")
            return l, c, r

#################### TODO : checks adjacency ####################
def isTileLegalOnBoard(app, l, c, r):
    ''' Given tile index on board, 
        Returns boolean value of whether tile is legal 
        (there isn't any existing tile on board
         and meets adjacency constraints with 6 neighboring tiles '''
    # Checks existing
    if app.board_tiles[l,c,r] == 1: return False
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
    
    drawBoard(app) 

    drawTileSet(app)

    drawMovingTile(app)

    # # test map to pixel
    # print(f'origin: {app.grid_ix, app.grid_iy}')
    # print(f'map to pixel test : origin {tileOnBoardOrigin(1,0,0, app.grid_ix, app.grid_iy, app.tileDim)}')
    # print(f'map to pixel test : 1,0 {tileOnBoardOrigin(1,0,0, app.grid_ix, app.grid_iy, app.tileDim)}')
    # drawCircle(*tileOnBoardOrigin(1,0,0, app.grid_ix, app.grid_iy, app.tileDim), 3, fill='red')

    # drawTileOnGrid(app)

    # compile all tiles , put all cubes into 3d grid
    # draw faces while checking occlusion 

    ### TEST : draw functions ###
    # drawIsoRect(100, 100, 50, 50)
    # drawIsoGrid(600, 100, 5, 5, 50)
    # drawCartGrid(100, 100, 5, 5, 50)
    # drawIsoCube(600, 100, 50, 50, 50) # level 0
    # drawIsoCube(600, 50, 50, 50, 50)  # level -1
    # drawIsoCube(600, 150, 50, 50, 50) # level 1 
    
    
    # mapToCube(map, 600, 100, 50)
    # drawGrid(app)
    # drawCube(app)

    ## TODO ##    
    # select tiles > move on iso grid > shadow show

        
## Isometric Functions ##

def cartToIso(x, y):
    isoX = x - y
    isoY = (x+y)/2
    return int(isoX), int(isoY)
    
def isoToCart(ix, iy):
    cx = (ix + 2*iy)/2
    cy = (-ix + 2*iy)/2
    return int(cx), int(cy)

def tileIndexToPixel(app, l, c, r):
    '''Given 3d board coordinate of tile unit l, c, r,
    Return pixel coordinate of origin point(center) tx, ty
    isometric width is 2*tileDim and height is 1*tileDim
    Make sure that pixel value is integer!
    '''
    d = app.tileDim
    tx = app.grid_ix + r*d - c*d 
    ty = app.grid_iy + r*0.5*d + c*0.5*d - l*d
    return int(tx), int(ty)

      
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

def mapToCube(map, ix, iy, d): ####### NO USE
    ''' Given map, isometric pixel origin coordinate(top point of level 0), dimension of cube
        draw cube on non board'''
    i_w = 2*d
    i_h = d
    # take in map of rows*cols*level dimension and draw cubes
    # how does ix, iy (bottomleft) change?
    # drawIsoCube(ix, iy, w, d, h)
    # l >> ix          , iy - l*d
    # r >> ix - r*i_w/2, iy + r*i_h/2
    # c >> ix + c*i_w/2, iy + c*i_h/2
    
    # Numpy version
    levels, rows, cols = np.shape(map)
    cubeInds = np.argwhere(map == 1)
    for l,r,c in cubeInds:
        t_ix = ix - r*i_w/2 + c*i_w/2  
        t_iy = iy - l*d + r*i_h/2 + c*i_h/2
        drawIsoCube(t_ix, t_iy, d, d, d)

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

def drawIsoGrid(ix, iy, rows, cols, d, b='gray', f=None, label=False, b_w=0.5):
    ''' Given top pixel coordinate cx, cy of isometric grid
        ,number of rows and columns, and cell dimension, draw isometric grid '''
    i_w = 2*d
    i_h = d
    for r in range(rows):
        for c in range(cols):
            x = ix + 0.5*i_w*(r-c)
            y = iy + 0.5*i_h*r + 0.5*i_h*c
            # print(f'** Top of tile {r},{c} = ({x},{y})')
            drawIsoRect(x, y, d, d, b, f, b_w=b_w)
            if label:
                drawLabel(f"{r},{c}", x, y+0.5* i_h, size=10, font='arial', 
                        fill="blue", opacity=80)    

def drawCartGrid(cx, cy, rows, cols, d): ####### NO USE
    for r in range(rows):
        for c in range(cols):
            drawRect(cx+r*d,cy+c*d, d, d, border='black', borderWidth=1, fill=None, opacity=40)
            drawLabel(f"{r},{c}", cx+r*d +0.5*d, cy+c*d + 0.5*d, size=10, font='arial', 
                      fill="orange", opacity=80)
                      
## Tile Functions ##
# 1. Tile set window
def drawTileOnCanvas(app, tile, px, py):
    '''Given Tile object, and pixel coordinate(bottom side top point)
        draw cubes according to tile map
        Used to draw tile set'''

    ### integrating mapToCube(tile.map, px, py, app.cubeDim)
    i_w = 2*app.cubeDim
    i_h = app.cubeDim

    # Numpy version
    levels, rows, cols = np.shape(tile.map)
    cubeInds = np.argwhere(tile.map == 1)
    for l,r,c in cubeInds:
        # print(f'drawing tiles... {l} {r} {c} of tile map')
        # pixel coordinate of cube origin (bottom top)
        tx = px - r*i_w/2 + c*i_w/2  
        ty = py - l*app.cubeDim + r*i_h/2 + c*i_h/2

        ## integrating drawIsoCube(t_ix, t_iy, d, d, d) so that draw less shapes
        tt, tr, tb, tl = getCornerPointsIsoRect(tx, ty-app.cubeDim, app.cubeDim, app.cubeDim)
        bt, br, bb, bl = getCornerPointsIsoRect(tx, ty, app.cubeDim, app.cubeDim)

        if l==levels-1 or tile.map[l+1, r, c] != 1:
            drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='white') # draw top    
        if r==rows-1 or tile.map[l, r+1, c] != 1:
            drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='gray') # draw left front
        if c==cols-1 or tile.map[l, r, c+1] != 1:
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

        # draw tile
        drawTileOnCanvas(app, tile, px, py)

        # draw guide boundary
        drawTileBound(app, tile)

        # place holder region
        drawPolygon(px-0.5*ph_w, py-0.5*ph_h, px+0.5*ph_w, py-0.5*ph_h, 
                    px+0.5*ph_w, py+0.5*ph_h, px-0.5*ph_w, py+0.5*ph_h, borderWidth=1,
                    fill=None, border='yellowGreen', dashes=True)

def drawTileBound(app, tile, b='cyan', b_w=1, o=80, d=(1,2)):
    # from caresian rect > get corners of iso rectangles
    tt, tr, tb, tl = getCornerPointsIsoRect(tile.px, tile.py-app.tileDim, app.tileDim, app.tileDim)
    bt, br, bb, bl = getCornerPointsIsoRect(tile.px, tile.py, app.tileDim, app.tileDim)
    # Transparent
    drawPolygon(*tt, *tr, *tb, *tl, border=b, borderWidth=b_w, fill=None, opacity=o, dashes=d) # top
    drawPolygon(*tt, *tr, *tb, *tl, border=b, borderWidth=b_w, fill=None, opacity=o, dashes=d) # bottom
    drawPolygon(*tl, *bl, *bb, *tb, border=b, borderWidth=b_w, fill=None, opacity=o, dashes=d) # left front
    drawPolygon(*tb, *tr, *br, *bb, border=b, borderWidth=b_w, fill=None, opacity=o, dashes=d) # right front
    drawPolygon(*tl, *tt, *bt, *bl, border=b, borderWidth=b_w, fill=None, opacity=o, dashes=d) # left back
    drawPolygon(*tt, *tr, *br, *bt, border=b, borderWidth=b_w, fill=None, opacity=o, dashes=d) # right back

# 2. Tile 

def placeTileOnBoard(app, tile, l, c, r):
    ''' Given the board coordinate of bottom side top cube (in isometric view) of tile,
        place tile on board by placing valid cube
        '''
    # replace part of board map with tile map
    # print(f'board shape is {app.board.shape} and tile shape is {tile.map.shape}')
    app.board[l:l+tile.size, c:c+tile.size, r:r+tile.size] = tile.map
    app.board_tile[l,c,r] = 1
    # set tile location value
    tile.onBoard = True
    tile.l, tile.c, tile.r = l, c, r
    tile.px, tile.py = -1, -1 # clearing values if any

def drawBoard(app):
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
    drawIsoGrid(app.grid_ix, app.grid_iy, app.rows, app.cols, app.tileDim, label=True) # level 0 tile grid in default lines
    drawIsoGrid(app.grid_ix, app.grid_iy, app.rows*app.tileSize, app.cols*app.tileSize, app.cubeDim, 
                b='lightgray', b_w = 0.2) # level 0 cube grid in lighter and thinner lines
    for level in range(1,app.levels+1):
        drawIsoGrid(app.grid_ix, app.grid_iy-app.tileDim*level, app.rows, app.cols, app.tileDim, b_w=0.2, label=False) # level 1~tile grid
    
    # board size in units of cubes
    levels, rows, cols = app.levels, app.rows, app.cols
    i_w = 2*app.cubeDim
    i_h = app.cubeDim

    # go over cubes on board, check if face occluded, draw only when displayed
    cubeInds = np.argwhere(app.board == 1)
    for z,y,x in cubeInds:
        cx = app.grid_ix - x*i_w/2 + y*i_w/2 
        cy = app.grid_iy - z*app.cubeDim + x*i_h/2 + y*i_h/2
        bt, br, bb, bl = getCornerPointsIsoRect(cx, cy, app.cubeDim, app.cubeDim)
        tt, tr, tb, tl = getCornerPointsIsoRect(cx, cy-app.cubeDim, app.cubeDim, app.cubeDim)

        if z==levels-1 or app.board[z+1, x, y] != 1:
            drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='white') # draw top    
        if x==rows-1 or app.board[z, x+1, y] != 1:
            drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='gray') # draw left front
        if y==cols-1 or app.board[z, x, y+1] != 1:
            drawPolygon(*tb, *tr, *br, *bb, border='white', borderWidth=0.3, fill='black') # draw right front

def drawMovingTile(app):
    # if holding tile, draw current tile *bottom side left cube* on mouse position
    # (to visualize better!)
    if app.holdingTile:
        if not app.currentTile.onBoard: # not on board
            drawTileOnCanvas(app, app.currentTile, app.currentTile.px, app.currentTile.py)
        else:
            drawTileOnBoard(app, app.currentTile, app.currentTile.l, app.currentTile.c, app.currentTile.r)
        

    # add rotation?

def drawTileOnBoard(app, tile, l, c, r):
    '''Given Tile object, and board_tile index
        draw cubes according to tile map and bounding box
        Used to draw holding tile on board'''
    tx, ty = tileIndexToPixel(app, l, c, r)
    drawTileOnCanvas(app, tile, tx, ty)
    drawTileBound(app, app.currentTile)

def main():
    runApp(1200, 600)

main()