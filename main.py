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
    app.tileSize = S["tileSize"]
    app.cubeDim = S["cubeDim"]
    app.tileDim = S["tileDim"]
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
    app.drawnTiles = []
    app.displayFaceArgs=[] # list of polygons arguments to draw

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
    
    
    drawBackground(app) 

    drawTileSet(app)

    drawTileOnGrid(app)

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

def drawBackground(app):
    ''' Draw isometric grid on right side, and tile set window on left side'''
    # # iso grid 
    drawRect(app.gridWin_l, app.gridWin_t, app.gridWin_w, app.gridWin_h,
             border='skyBlue', fill=None)
    grid_cx, grid_cy = app.gridWin_l + app.gridWin_w/2, app.gridWin_t + app.tileDim * (app.levels + 2)
    # drawIsoGrid(cx, cy, rows, cols, d, b='gray', f=None, label=False, b_w=0.5)
    drawIsoGrid(grid_cx, grid_cy, app.rows, app.cols, app.tileDim, label=True) # level 0 tile grid
    drawIsoGrid(grid_cx, grid_cy, app.rows*app.tileSize, app.cols*app.tileSize, app.cubeDim, 
                b='lightgray', b_w = 0.2) # level 0 cube grid
    for level in range(1,app.levels+1):
        drawIsoGrid(grid_cx, grid_cy-app.tileDim*level, app.rows, app.cols, app.tileDim, b_w=0.2, label=False) # level 1~tile grid
    
    # # tile set window
    drawRect(app.tileWin_l, app.tileWin_t, app.tileWin_w, app.tileWin_h,
             border='darkSeaGreen', fill=None)

    # (temp) display 2d -> 2.5d mapping
    # drawCartGrid(app.tileWin_l+25, app.tileWin_t+25, app.rows, app.cols, app.tileDim)


        
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
    # ix, iy is top left point of cartesian rect
    # equates to top point of isometric rect
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
    # cx , cy is start of index 0,0 at top of grid 
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
    return [(iso_t_x, iso_t_y), (iso_r_x, iso_r_y), (iso_b_x, iso_b_y), (iso_l_x, iso_l_y)]
    
def drawIsoGrid(cx, cy, rows, cols, d, b='gray', f=None, label=False, b_w=0.5):
    ''' Given top point cx, cy and number of rows and columns, draw isometric grid '''
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
    ''' Draw faces as polgons from app.displayFaceArgs.
        This reduces the number of shapes we need to draw 
        app.board = np.array (app.levels*app.tileSize, app.rows*app.tileSize, app.cols*app.tileSize)) 
        level = b_z, row = b_x, col = b_y 
        '''
    # board size in units of cubes
    height, width, depth = np.shape(app.board)

    # go over cubes on board, check if face occluded, draw only when displayed
    cubeInds = np.argwhere(app.board == 1)
    for z,y,x in cubeInds:
        
        tt, tr, tb, tl, bt, br, bb, bl = getCubeCorners(z,y,x)

        if app.board[z+1,y,x] != 1:
            pass# draw top
        if app.board[z,y+1,x] != 1:
            pass# draw left
        if app.board[z,y,x+1] != 1:
            pass# draw right

        # app.displayFaceArgs
        #drawIsoCube(t_ix, t_iy, d, d, d)
        tt, tr, tb, tl = getCornerPointsIsoRect(ix, iy-h, w, d)
        bt, br, bb, bl = getCornerPointsIsoRect(ix, iy, w, d)
        # Opaque
        drawPolygon(*tt, *tr, *tb, *tl, border='black', borderWidth=0.3, fill='white') # top
        drawPolygon(*tl, *bl, *bb, *tb, border='black', borderWidth=0.3, fill='gray') # left front
        drawPolygon(*tb, *tr, *br, *bb, border='white', borderWidth=0.3, fill='black') # right front

def getCubeCorners(z,y,x):
    # get 6 points of cube by
    # level + 1 changes py -> py+h 
    # from caresian rect > get corners of iso rectangles
    px, py = boardToPixel(z,y,x)
    tt, tr, tb, tl = getCornerPointsIsoRect(px, py-h, w, d)
    bt, br, bb, bl = getCornerPointsIsoRect(px, py, w, d)

def boardToPixel(z,y,x):
    ''' Given board coordinate, and top point of board grid, return pixel coordinate of top point of cube'''

def main():
    runApp(1200, 600)

main()