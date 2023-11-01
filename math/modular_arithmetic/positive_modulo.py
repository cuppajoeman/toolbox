"""
For m > 0, then we take x % m, which is in the range [-m + 1, m -1],
then add m to it, the reason why we take the mod again is because if
x % m >= 0, then adding m pushes it out of the range again
"""
def pos_mod(x,m):
    return (x%m + m)%m
