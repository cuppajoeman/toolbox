width = 10
height = 20

grid = [[f'({x}, {y})' for x in range(width)] for y in range(height)]

x, y = 3, 4

cell_3_4 = grid[x][y]

print(cell_3_4) # prints (4, 3) which is wrong which doesn't match our intuition.

# when making a 2d array it's best to think about how you want to access the data in the array
# for example when we do grid[x][y], we'd like to get the element (x, y), the reason why this doesn't
# happen in the above configuraiton is because we can think of the 2d array as this
# grid = [[(1, 1), (2, 1), ..., (width - 1, 1)], [(1, 2), (2, 2), ..., (width - 1, 2)], ..., [(1, height - 1), (2, height - 1), ..., (width - 1, height - 1)]]
# and thus we can re-arrange it like this:
#
# [
#     [(1, 1), (2, 1), ..., (width - 1, 1)], 
#     [(1, 2), (2, 2), ..., (width - 1, 2)], 
#     ..., 
#     [(1, height - 1), (2, height - 1), ..., (width - 1, height - 1)]
# ]
# 
# which is the start/canonical way of viewing a matrix
# 
# in our case grid[i] is the i-th row of the matrix, which corresponds to the y aspect of this matrix, 
# this implies that grid[i][j] would be G_{j,i} with respect to regular matrix indexing, which is very confusing!
#
# Therefore an easy fix to this is to instead always construct the transpose of this matrix like this

# [
#     [(1, 1), (2, 1), ..., (height - 1, 1)], 
#     [(1, 2), (2, 2), ..., (height - 1, 2)], 
#     ..., 
#     [(1, width - 1), (2, width - 1), ..., (height - 1, width - 1)]
# ]
#
# and with this grid we have that grid[i][j] is G_{i,j}
#
# with this setup, you can think of each inner array as being a column of the matrix. and therefore G[i] selects a column first (x aspect of the matrix)

grid = [[f'({x}, {y})' for y in range(height)] for x in range(width)]

x, y = 3, 4

cell_3_4 = grid[x][y]

print(cell_3_4) # prints (4, 3) which is wrong, so what's wrong?
