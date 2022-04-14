from cmu_cs3_graphics import *
import numpy as np
import settings 
import tile
import copy

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
    app.board = np.zeros((app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize))

    # top pixel coordinate of background grid at level 0
    app.grid_ix, app.grid_iy = app.gridWin_l + app.gridWin_w/2, app.gridWin_t + app.tileDim * (app.levels + 2)
    app.grid_cx, app.grid_cy = isoToCart(app.grid_ix, app.grid_iy)




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
        [[1,1,1],
         [0,1,0],
         [1,1,0]],
        [[1,1,1],
         [0,0,1],
         [0,0,1]]
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
    test_tileset = [test_tile] * 9
    app.tileSet = test_tileset


## Functions used on start
def initializeBoard(app):
    # returns empty isometric grid
    return 42

## Controllers

def onKeyPress(app, key):
    if key == 'q':
        return 42

def onMousePress(app, mouseX, mouseY):
    # check if legal place
    # if legal, change location of tile 
    ## Test ##
    # to see max shape size + try drawing on grid
    new_tile = copy.deepcopy(app.tileSet[0]) # is copy valid?
    new_tile.px, new_tile.py = mouseX, mouseY
    app.drawnTiles.append(new_tile)
    

## Draw
def redrawAll(app):
    
    
    drawBoard(app) 

    drawTileSet(app)

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
      
def drawIsoCube(px, py, w, d, h):
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
    
    # print(*tt)
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
    
def drawIsoGrid(cx, cy, rows, cols, d, b='gray', f=None, label=False, b_w=0.5):
    ''' Given top pixel coordinate cx, cy of isometric grid
        ,number of rows and columns, and cell dimension, draw isometric grid '''
    i_w = 2*d
    i_h = d
    for r in range(rows):
        for c in range(cols):
            x = cx + 0.5*i_w*(r-c)
            y = cy + 0.5*i_h*r + 0.5*i_h*c
            # print(f'** Top of tile {r},{c} = ({x},{y})')
            drawIsoRect(x, y, d, d, b, f, b_w=b_w)
            if label:
                drawLabel(f"{r},{c}", x, y+0.5* i_h, size=10, font='arial', 
                        fill="blue", opacity=80)    

def drawCartGrid(cx, cy, rows, cols, d):
    for r in range(rows):
        for c in range(cols):
            drawRect(cx+r*d,cy+c*d, d, d, border='black', borderWidth=1, fill=None, opacity=40)
            drawLabel(f"{r},{c}", cx+r*d +0.5*d, cy+c*d + 0.5*d, size=10, font='arial', 
                      fill="orange", opacity=80)
                      
## Tile Functions ##
def drawTile(app, tile, px, py):
    '''given Tile object, draw tile according to map'''
    t_map = tile.map
    mapToCube(t_map, px, py, app.cubeDim)

def mapToCube(map, ix, iy, d):
    ''' takes in map, start position of map (bottom left pixel coordinate), dimension of cube'''
    i_w = 2*d
    i_h = d
    # take in map of rows*cols*level dimension and draw cubes
    # how does ix, iy (bottomleft) change?
    # drawIsoCube(ix, iy, w, d, h)
    # l >> ix          , iy - l*d
    # r >> ix - r*i_w/2, iy + r*i_h/2
    # c >> ix + c*i_w/2, iy + c*i_h/2
    
    # # Python version
    # levels = len(map)
    # rows = len(map[0])
    # cols = len(map[0][0])
    
    # for l in range(levels):
    #     for r in range(rows):
    #         for c in range(cols):
    #             if map[l][r][c] == 1:
    #                 t_ix = ix - r*i_w/2 + c*i_w/2
    #                 t_iy = iy - l*d + r*i_h/2 + c*i_h/2
    #                 drawIsoCube(t_ix, t_iy, d, d, d)
    
    # Numpy version
    levels, rows, cols = np.shape(map)
    cubeInds = np.argwhere(map == 1)
    for l,r,c in cubeInds:
        t_ix = ix - r*i_w/2 + c*i_w/2  
        t_iy = iy - l*d + r*i_h/2 + c*i_h/2
        drawIsoCube(t_ix, t_iy, d, d, d)

def drawTileSet(app):
    ''' Draws tile set on left side of page'''
    # tile set window
    drawRect(app.tileWin_l, app.tileWin_t, app.tileWin_w, app.tileWin_h,
             border='darkSeaGreen', fill=None)


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
    for i in range(len(app.tileSet)):
        tile = app.tileSet[i]
        row_i = i//3
        col_i = i%3
        px = l + col_i*1.25*ph_w+ph_w/2 # start + column index * (ph_w + 0.25*ph_(margin)) + ph_w/2
        py = t + row_i*1.25*ph_h+ph_h/2

        # place holder region
        drawPolygon(px-0.5*ph_w, py-0.5*ph_h, px+0.5*ph_w, py-0.5*ph_h, 
                    px+0.5*ph_w, py+0.5*ph_h, px-0.5*ph_w, py+0.5*ph_h, 
                    fill=None, border='yellowGreen', dashes=True)

        drawTile(app, tile, px, py)
        
# (temp) to test drawing tiles onMousePress
def drawTileOnGrid(app):
    for tile in app.drawnTiles:
        # add tile to board
        # check for occlusion 
        drawTile(app, tile, tile.px, tile.py)

# TODO: rearrange drawing to draw on board -------------------------------------------------------------
def placeTileOnBoard(app, tile):
    ''' Given the board coordinate of top (in isometric view) cube of tile,
        place tile on board by placing valid cube'''
    # replace part of board map with tile map
    app.board[tile.x:tile.x+tile.size, tile.y:tile.y+tile.size, tile.z:tile.z:tile.size] = tile.map

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
    # height, width, depth = np.shape(app.board)

    # go over cubes on board, check if face occluded, draw only when displayed
    cubeInds = np.argwhere(app.board == 1)
    for z,y,x in cubeInds:
        bt, br, bb, bl, tt, tr, tb, tl = getCubeCorners(z,y,x)
        if app.board[z+1,y,x] != 1:
            drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='white') # draw top    
        if app.board[z,y+1,x] != 1:
            drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='gray') # draw left front
        if app.board[z,y,x+1] != 1:
            drawPolygon(*tb, *tr, *br, *bb, border='white', borderWidth=0.3, fill='black') # draw right front

    # (temp) display 2d -> 2.5d mapping
    # drawCartGrid(app.tileWin_l+25, app.tileWin_t+25, app.rows, app.cols, app.tileDim)



def getCubeCorners(z,y,x):
    ''' Given index z,y,x of cube on board,
        Return pixel coordinates of 6 points of cube.
        '''
    # cube points start from bottom left!
    # z changes in iso == -y in pixel space 
    
    bt, br, bb, bl = getCornerPointsIsoRect(app.grid_cx, app.grid_cy, app.tileDim, app.tilDim)
    tt, tr, tb, tl = getCornerPointsIsoRect(app.grid_cx, app.grid_cy-app.tileDim, app.tileDim, app.tileDim)

    return bt, br, bb, bl, tt, tr, tb, tl






def main():
    runApp(1200, 600)

main()