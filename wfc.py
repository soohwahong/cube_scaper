import numpy as np
from tileSetB import * 

'''
TODO
1. Implement WFC
    - Output board
        - every tile on outbut board initialized with all (tile, rotation)
    - Observed board
        - keep track of locations that have been input
    - Input tile 
        - manually input
        - from end nbr
            - if nbr exists(preset constraints), check if match -> if not backtrack
            - if nbr not exists, set neighbor that matches

    *- Propogate (forward checking)
        - for neighboring 6 location : nbr
            - for each (tile,rotation) in output[nbr] eliminate non-possible 
                - for nbr.start neighboring 3 sides, eliminate (tile, rotate)
            - if any tile eliminated from nbr, check nbr's 3 nbrs until no change
    
    - Terminate
        - generation (when no possible neighbors)
        - maze (meet goal tile)
    - check all 4 rotations for tile, if does not fit, eliminate

2. Form Tileset with constraints
    - start and end designation attribute for tile
        - 8 possible positions
        - (start, end) pairs : same tile, same x axis, y axis, z axis
    
    - d(+x, -x, +y, -y, +z, -z)?
    - None(empty) tile (can designate up front for maze generation)
'''

# Create tile set
# display propagation of available tiles
# implement function
