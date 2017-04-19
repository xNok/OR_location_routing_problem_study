
from pkg.cplex_solve import cplex_solve
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library

def tcflp_cplex(I,V1,V2,
            c,f,
            q,V,
            relaxation=False,path=None):
    """
    I,J,C sets of customers, ICPs, CRCs
    c,f cost matrix for connection and setup
    """
    #####################################################################
    # Decision variables
    
    def X(i,j1):
        return "X_" + str(i) + "_" + str(j1)
    
    def Y(j1,j2):
        return "X_" + str(j1) + "_" + str(j2)

    def Z(j,r):
        return "Z_" + str(j) + "_" + str(r)

    #####################################################################
    # Objective function
    
    objx = [c[0][i][j1]  for i in range(I) for j1 in range(V1) for j2 in range(V2)]
    objy = [c[1][j1][j2] for j1 in range(V1) for j2 in range(V2)]
    objz = [f[j] for j in range(V1+V2)]
    
    ## variablesnames
    Xs = [X(i,j1) for i in range(I) for j1 in range(V1)]
    Ys = [Y(j1,j2) for j1 in range(V1) for j2 in range(V2)]
    Zs = [Z(j,1) for j in range(V1)] + [ Z(j,2) for j in range(V2)]

    ## Objective function sum aggregation
    obj = objx + objy + objz
    colnames = Xs + Ys + Zs
    if relaxation:
        types    = "C" * (I*V1+V1*V2+(V1+V2)) #Integrality constraint
    else:
        types    = "I" * (I*V1+V1*V2+(V1+V2)) #Integrality constraint

    #####################################################################
    # Constraints
    
    c1 = [
            [[X(i,j1) for j1 in range(V1)],[1 for j1 in range(V1)]]
          for i in range(I)]
    c2 = [
            [[Y(j1,j2) for j2 in range(V2)]+[X(i,j1) for i in range(I)], [1 for j2 in range(V2)]+[-1 for i in range(I)]]
          for j1 in range(V1)]
    c3 = [
            [[Y(j1,j2) for j1 in range(V1)]+[Z(j2,1)], [1 for j1 in range(V1)]+[-V[0][j1]]]
          for j2 in range(V2)]
    c4 = [
            [[Y(j1,j2) for j2 in range(V2)]+[Z(j2,2)], [1 for j2 in range(V2)]+[-V[1][j1]]]
          for j1 in range(V1)]
    
    s1 = "G" * I
    s2 = "G" * V1
    s3 = "L" * V2
    s4 = "L" * V1
    
    r1 = [q[i] for i in range(I)]
    r2 = [0 for j1 in range(V1)]
    r3 = [0 for j2 in range(V2)]
    r4 = [0 for j1 in range(V1)]
    
    rows = c1+c2+c3+c4
    senses = s1+s2+s3+s4
    rhs =  r1+r2+r3+r4
    
    #####################################################################
    # Bounds
    ub = None
    lb = [0 for i in range(I*V1+V1*V2+(V1+V2))]

    #####################################################################
    # Solving
    prob = cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=path)

    #####################################################################
    # Extract solution
    solution = prob.solution.get_values()
    X = np.reshape(solution[0:I*V1*V2],(I,V1,V2))
    Z = solution[I*V1*V2:]

    return prob, X, Z