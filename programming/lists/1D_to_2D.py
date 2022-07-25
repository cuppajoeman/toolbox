def convert_var_len(lst, var_lst): 
    idx = 0
    for var_len in var_lst: 
        yield lst[idx : idx + var_len] 
        idx += var_len 

def convert_same_len(lst, row_size):
    for i in range(0, len(lst), row_size):
        yield lst[i: i + row_size]

# Driver code 
#lst = [1, 2, 3, 4, 5, 6] 
#var_lst = [1, 2, 3] 
#print(list(convert(lst, var_lst))
#[[1], [2, 3], [4, 5, 6]]

