def chunk_list(l,n):
    return [data[x:x+n] for x in range(0, len(data), n)]
