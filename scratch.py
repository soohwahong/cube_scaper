import numpy as np

map = [
        [[1,0,0],
         [0,1,0],
         [0,0,1]],
        [[0,0,1],
         [0,1,0],
         [1,0,0]]
      ]

map = np.array(map)
      
# print(f'shape is {np.shape(map)}')
# print(f'1s are at {np.where(map == 1)}')
# print(f'1s are at (argwhere format) {np.argwhere(map == 1)}')
# print(f'all array (argwhere format with no condition) {np.argwhere(((map==0) | (map==1)))}')
# cubeInds = np.argwhere(map == 1)
# for l,r,c in cubeInds:
#     print(f'level : {l}, row:{r}, col:{c}')

# np.arange(start, stop, step, dtype)
# np.reshape(array, shape)
# np.arage(8).reshape(4,2)

# np.shape()

# Initial Array
arr = np.array([[-1, 2, 0, 4],
                [4, -0.5, 6, 0],
                [2.6, 0, 7, 8],
                [3, -7, 4, 2.0]])
# Printing a range of Array
# with the use of slicing method
sliced_arr = arr[:2, ::2]
# print ("Array with first 2 rows and"
#     " alternate columns(0 and 2):\n", sliced_arr)

# Printing elements at
# specific Indices
Index_arr = arr[[1, 1, 0, 3], 
                [3, 2, 1, 0]]
# print ("\nElements at indices (1, 3), "
#     "(1, 2), (0, 1), (3, 0):\n", Index_arr)

# arr.sum()

## Datatypes : int64, float64
x = np.array([1,2], dtype=np.int64)
x.dtype

# numpy.zeros(shape, dtype=float)


# replace part of array
full_five = np.zeros((5,5,5))
print(f'Original: \n{full_five}')
replace = np.array([
    [1,1,1],
    [1,1,1],
    [1,1,1]
])
a, b, c = 0, 1, 2
full_five[a:a+3, b:b+3, c:c+3] = replace
print(f'After replacing:\n{full_five}')