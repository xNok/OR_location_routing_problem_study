
import numpy as np

def swap_list_byRoute(Y,W,DjUc,N_icp,routes):
    """
        find the 2 routes and arcs to swap
        find wich elemtent to swap with which other element
    """
    cluster_len = np.max(np.multiply(Y,W),axis=0)
    swaps = []
    for iroute,route in enumerate(routes):
        for iarc,arc in enumerate(route): #chose on element
            if arc[0] < len(cluster_len): # do not select CRC
                for j_bis,n in enumerate(DjUc[arc[0]]): # look at other
                    if j_bis < len(cluster_len):
                        if n<cluster_len[arc[0]] and cluster_len[j_bis] == 0 and arc[0] != j_bis:
                            coarc = [[iroute, ico] for ico,co in enumerate(route) if co[1] == arc[0]]
                            swaps.append(([iroute,iarc],coarc[0],arc[0],j_bis))         
    return swaps