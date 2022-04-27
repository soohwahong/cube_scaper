Cube Scaper
    This project is a constraint based 2.5D world generation. 
    It involves a set of tiles in the form of cubical 2.5D isometric geometry and the Wave Function Collapse algorithm (WFC) (Gumin,2016) 
    to place tiles according to the tile set’s connectivity rules.

To Run:
    main.py

    Dependencies:
    cmu_cs3_graphics
    numpy
    settings 
    copy
    matplotlib
    random
    isometric
    tile
    tileSetB (default tile set)

Instructions:
    0. Select Mode (Path / Pattern)

Pattern Mode
    1. Click on tile to select and place on board
        - green indicates valid location
        - red indicates invalid location
    2. Observe reduced neighbors on level guide
    3. Press R to clear board
    4. Press Z to select modified tile set.
    5, Press Z to finalize tile set.
    6. Press W to generate pattern
    7. Press → to rotate board and view from all sides. 
    8. Press R to clear board and tile set. 

Path Mode 
    1. Press S to set START tile. Click and place on board
    2. Press E to set END tile. Click and place on board
    3. Place other tiles on board.
    4. Press P to check if there is valid path from START to END
        - If path exists, it will show in red.
    6. Press → to rotate board and view from all sides. 
    7. Press R to clear board and START and END. 

Keys: 
    # At Start Screen
        0 : Pattern Mode
        1 : Path Mode
    # Common
        H : Return to home
        R : Clear all
        L : Toggle level guide
        ↑ ↓ : Control level guide 
        → : Rotate board (use after generation)
    # Pattern Mode
        Z : Toggle select tile mode
        W : Generate pattern
    # Path Mode
        S : Set START tile
        E : Set END tile
        P : Generate Tile

