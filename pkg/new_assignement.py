
import numpy as np

def new_assignement(I,J,W,N_icp_swap):
    H1 = [j for j,vj in enumerate(N_icp_swap) if vj > 0.5]
    asso = np.argmin(np.transpose(W)[H1],axis=0)
    new_Y = np.zeros((I,J))
    for a,va in enumerate(asso):
        new_Y[a][H1[va]] = 1
    return new_Y