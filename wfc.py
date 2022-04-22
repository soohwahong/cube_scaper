'''Implements Wave function Collapse'''

'''
TODO
1. Implement WFC
    - Output board
        - every tile on outbut board initialized with all (tile, rotation)
    - Input tile 
        - manually input
        - randomly choose from output board possibility
    - Propogate (forward checking)
        - for neighboring 6 location : nbr
            - for each (tile,rotation) in output[nbr] (in what order?), check adjacency
                - for nbr.end side(3 sides) - check match : if input.end meets nbr.start
                - for non end sides(3 sides) - check non-match : start, end cannot be on that side??? 
                - if not match, eliminate nbr from output[nbr]
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