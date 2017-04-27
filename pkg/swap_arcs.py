
import numpy as np

def swap_arcs(swap, routes, N):
    routes_swap = np.copy(routes)
    N_swap = N[:]
    remove = swap[2]
    introduce = swap[3]
    
    print("swap: %s %s" % (remove,introduce))

    arc1 = routes_swap[swap[0][0]][swap[0][1]]
    arc2 = routes_swap[swap[1][0]][swap[1][1]]

    if arc1[0] == remove:
        arc1 = (introduce, arc1[1])
    else:
        arc1 = (arc1[0], introduce)

    if arc2[0] == remove:
        arc2 = (introduce, arc2[1])
    else:
        arc2 = (arc2[0], introduce)

    routes_swap[swap[0][0]][swap[0][1]] = arc1
    routes_swap[swap[1][0]][swap[1][1]] = arc2
    N_swap[remove] = 0
    N_swap[introduce] = 1

    return routes_swap, N_swap