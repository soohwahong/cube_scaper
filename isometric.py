from cmu_cs3_graphics import *

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


def drawCartGrid(cx, cy, rows, cols, d): ####### NO USE
    for r in range(rows):
        for c in range(cols):
            drawRect(cx+r*d,cy+c*d, d, d, border='black', borderWidth=1, fill=None, opacity=40)
            drawLabel(f"{r},{c}", cx+r*d +0.5*d, cy+c*d + 0.5*d, size=10, font='arial', 
                      fill="orange", opacity=80)