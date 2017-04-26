
import numpy as np
from pkg.capacity_vector import capacity_vector

def capacity_balancing(Y,W,U,J,Q,N_icp):
    l = len(capacity_vector(Y,U,J,Q)[1])
    max_loop = 10;

    # capacity balancing
    Ycp = np.copy(Y)
    Wcp = np.copy(W)
    while l != 0 or max_loop == 0:
        max_loop +=-1
        j = capacity_vector(Ycp,U,J,Q)[1][0]
        i = np.argmax(np.multiply(Ycp,W)[:,j])
        # Find condidate and update
        Ycp[i][j] = 0
        Wcp[i][j] = 100
        stop = False
        while not stop:
            candidate = np.argmin(Wcp[i])
            if N_icp[candidate] > 0.5 and candidate != j:
                stop = True
            else:
                Wcp[i][candidate] = 200

        print(i,j,candidate)

        Ycp[i][candidate] = 1
        Wcp[i][candidate] = 100

        l = len(capacity_vector(Ycp,U,J,Q)[1])
        
    return Ycp