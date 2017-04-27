
import numpy as np

def swap_list_crc(Y,W,Dcc,N):
    cluster_len = np.max(np.multiply(Y,W),axis=0)
    print(cluster_len)
    swaps = []
    for j,l in enumerate(cluster_len):
        for j_bis,n in enumerate(Dcc[j]):
            if n<l and j_bis != j:
                swaps.append((j,j_bis))
    return swaps