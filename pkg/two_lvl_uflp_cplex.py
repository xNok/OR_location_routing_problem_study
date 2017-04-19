
import cplex
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library

def X(i,j1,j2):
    return "X_" + str(i) + "_" + str(j1) + "_" + str(j2)

def Z(j,r):
    "Z_" + str(j) + "_" + str(r)

def two_lvl_uflp_cplex(I,V1,V2,
            c,f
            relaxation=False,path=None):
    """
    I,J,C sets of customers, ICPs, CRCs
    c,f cost matrix for connection and setup
    """

    #####################################################################
    # Objective function
    
    objx = [c[i][j1][j2]  for i in range(I) for j1 in range(V1) for j2 in range(V2)]
    objz = [f[j][r] for j in range(V1+V2) for r in range(2)]
    

    ## variablesnames
    Xs = [ X(i,j1,j2) for i in range(I) for j1 in range(V1) for j2 in range(V2)]
    Zs = [ "Z_" + str(j) + "_" + str(r) for j in range(V1+V2) for r in range(2)]

    ## Objective function sum aggregation
    obj = objx + objz
    colnames = Xs + Zs
    if relaxation:
        types    = "C" * (I*V1*V2+2*(V1+V2)) #Integrality constraint
    else:
        types    = "I" * (I*V1*V2+2*(V1+V2)) #Integrality constraint

    #####################################################################
    # Constraints
    
    c1 = [
            [[X(i,j1,j2) for j1 in range(V1) for j2 in range(V2)], [1 for j in range(V1+V2)]] 
          for i in range(I)]
    c2 = [
            [[X(i,j1,j2) for j1 in range(V1)]+[Z(j2,1)], [1 for j1 in range(V1)]+ [-1]]
          for i in range(I) for j2 in range(V2)]
    c3 = [
            [[X(i,j1,j2) + str(j2) for j2 in range(V2)]+[Z(j1,1)], [1 for j2 in range(V2)]+ [-1]]
          for i in range(I) for j1 in range(V1)]
    
    s1 = "E" * I
    s2 = "L" * (I*V1)
    s3 = "L" * (I*V2)
    
    r1 = [1 for i in range(I)]
    r2 = [0 for i in range(I) for j2 in range(V2)]
    r3 = [0 for i in range(I) for j1 in range(V1)]
    
    rows = c1+c2+c3
    senses = s1+s2+s3
    rhs =  r1+r2+r3
    
    #####################################################################
    # Bounds
    ub = [1 for i in range(I*J+J*C+J+C)]
    lb = [0 for i in range(I*J+J*C+J+C)]

    #####################################################################
    # Solving
    prob = cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=path)

    #####################################################################
    # Extract solution
    solution = prob.solution.get_values()
    Y = np.reshape(solution[0:I*J],(I,J))
    X = np.reshape(solution[I*J:I*J+J*C],(J,C))
    N_icp = solution[I*J+J*C:I*J+J*C+J]
    N_crc = solution[I*J+J*C+J:I*J+J*C+J+C]

    return prob, X, Y, N_icp, N_crc