# https://stackoverflow.com/questions/31542843/inpolygon-examples-of-matplotlib-path-path-contains-points-method
import numpy as np
from matplotlib import path
from cmu_cs3_graphics import *


print('hello')
def redrawAll(app):
    def inpolygon(xq, yq, xv, yv):
        ''' xq, xq are 1d numpy arrays of coordinates that form polygon
            xv, yv are 1d numpy arrays of points that are being evaluated
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

    xq = np.array([50,110, 130 ,75])
    yq = np.array([51,49, 100, 90])
    xv = np.array([50, 100, 150, 100])
    yv = np.array([50, 0, 50, 100])
    print(inpolygon(xq, yq, xv, yv))

    allPoints = []
    for i in range(*xv.shape):
        allPoints.append(int(xv[i]))
        allPoints.append(int(yv[i]))
    print(*allPoints)
    drawPolygon(*allPoints)
    
    for i in range(*xq.shape):
        drawCircle(int(xq[i]), int(yq[i]), 3, fill='red')

runApp(500,500)

