
import numpy as np
from numpy import linalg as LA

def distance_matrices(datasets):
    """
    Return a dictionary containing all the distance matrices for a
    given instance of the problem
    """
    M = {}

    for dataset1 in datasets:
        d1 = datasets[dataset1]
        for dataset2 in datasets:
            d2 = datasets[dataset2]
            
            M[dataset1+dataset2] = np.zeros((d1["number"],d2["number"]))

            for i,ixy in enumerate(d1["coordinate"]):
                for j,jxy in enumerate(d2["coordinate"]):
                    M[dataset1+dataset2][i][j] = LA.norm(np.subtract(ixy,jxy))
                
    return M