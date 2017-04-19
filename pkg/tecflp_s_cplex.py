
from pkg.cplex_solve import cplex_solve
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library

def tecflp_s_cplex(I,V1,V2,
            c,f,h,
            q,V,
            relaxation=False,path=None):
    """
    I,J,C sets of customers, ICPs, CRCs
    c,f,h cost matrix for connection and setup
    q,V demand and capacity matrix
    """
    #####################################################################
    # Decision variables
    
    def X(i,j1):
        return "X_" + str(i) + "_" + str(j1)
    
    def T(j1,j2):
        return "X_" + str(j1) + "_" + str(j2)

    def Z(j):
        return "Z_" + str(j)
    
    nbr_var = I*V1*V2+V1*V2+V2
    I = range(I); V1 = range(V1); V2 = range(V2);
    
    #####################################################################
    # Objective function
    
    objx = [c[i][j1][j2]  for i in I for j1 in V1 for j2 in V2]
    objt = [h[j1][j2] for j1 in V1 for j2 in V2]
    objz = [f[j] for j in V2]
    
    ## variablesnames
    Xs = [X(i,j1) for i in I for j1 in V1]
    Ts = [T(j1,j2) for j1 in V1 for j2 in V2]
    Zs = [Z(j2) for j2 in V2]

    ## Objective function sum aggregation
    obj = objx + objy + objz
    colnames = Xs + Ts + Zs
    if relaxation:
        types    = "C" * (nbr_var) #Integrality constraint
    else:
        types    = "I" * (nbr_var) #Integrality constraint

    #####################################################################
    # Constraints
    
    c1 = [
            [[X(i,j1,j2) for j1 in V1 for j2 in V2], [1 for j1 in V1 for j2 in V2]] 
          for i in I]
    c2 = [
            [[X(i,j1,j2) for i in I], [d[i] for i in I]]
          for j1 in V1 for j2 in V2]
    c3 = [
            [[T(j1,j2) for j2 in V2], [1 for j2 in V2]]
          for j1 in V1]
    c4 = [
            [[X(i,j1,j2),T(j1,j2)], [1,-1]]
          for i in I for j1 in V1 for j2 in V2]
    c5 = [
            [[T(j1,j2),Z(j2)], [1,-1]]
          for j1 in V1 for j2 in V2]
    
    s1 = "E" * len(I)
    s2 = "L" * len(V1)+len(V2)
    s3 = "L" * len(V1)
    s4 = "L" * V1
    s4 = "L" * V1
    
    r1 = [1 for i in I]
    r2 = [V[j1] for j1 in V1 for j2 in V2]
    r3 = [1 for j1 in V1]
    r4 = [0 for i in I for j1 in V1 for j2 in V2]
    r5 = [0 for j1 in V1 for j2 in V2]

    
    rows = c1+c2+c3+c4
    senses = s1+s2+s3+s4
    rhs =  r1+r2+r3+r4
    
    #####################################################################
    # Bounds
    ub = [1 for i in range(nbr_var)]
    lb = [0 for i in range(nbr_var)]

    #####################################################################
    # Solving
    prob = cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=path)

    #####################################################################
    # Extract solution
    I = len(I); V1 = len(V1); V2 = len(V2);
    
    solution = prob.solution.get_values()
    X = np.reshape(solution[0:I*V1*V2],(I,V1,V2))
    H = solution[I*V1*V2:I*V1*V2+V1*V2]
    Z = solution[I*V1*V2+V1*V2:]

    return prob, X, H, Z