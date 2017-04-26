
def capacity_vector(Y,U,J,Q):
    cluster_q = np.zeros(J)
    violated = []
    for i,vi in enumerate(Y):
        for j,vj in enumerate(vi):
            cluster_q[j] += U[i]*Y[i][j]
    
    for j,vj in enumerate(cluster_q):
        if cluster_q[j] > Q[j]:
            violated.append(j)
            
    return cluster_q, violated