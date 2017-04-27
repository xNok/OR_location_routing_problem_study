import numpy as np

def swap_list_icp(Y,W,Djj,N):
    cluster_len = np.max(np.multiply(Y,W),axis=0)
    swaps = []
    for j,l in enumerate(cluster_len):
        for j_bis,n in enumerate(DjUc[j]):
            if n<l:
                print(j,j_bis,n,l)
                if j != j_bis and j_bis < len(N) and N[j_bis] == 0:
                    swaps.append((j,j_bis))
    return swaps