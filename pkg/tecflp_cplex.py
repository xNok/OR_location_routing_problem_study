
from pkg.cplex_solve import cplex_solve
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library

def tecflp_cplex(I,V1,V2,
            c,f,
            q,V,
            relaxation=False,path=None):
    """
    I,J,C sets of customers, ICPs, CRCs
    c,f cost matrix for connection and setup
    q,V demand and capacity of facilities
    """
    #####################################################################
    # Decision variables
    
    def X(i,j1,j2):
        return "X_" + str(i) + "_" + str(j1) + "_" + str(j2)

    def Z(j,r):
        return "Z_" + str(j) + "_" + str(r)
    
    nbr_var = I*V1*V2+(V1+V2)
    I = range(I); V1 = range(V1); V2 = range(V2);

    #####################################################################
    # Objective function
    
    objx = [c[i][j1][j2]  for i in I for j1 in V1 for j2 in V2]
    objz = [f[j] for j in range(len(V1)+len(V2))]
    
    ## variablesnames
    Xs = [ X(i,j1,j2) for i in I for j1 in V1 for j2 in V2]
    Zs = [ Z(j,1) for j in V1] + [ Z(j,2) for j in V2]

    ## Objective function sum aggregation
    obj = objx + objz
    colnames = Xs + Zs
    if relaxation:
        types    = "C" * nbr_var #Integrality constraint
    else:
        types    = "I" * nbr_var #Integrality constraint

    #####################################################################
    # Constraints
    
    c1 = [
            [[X(i,j1,j2) for j1 in V1 for j2 in V2], [1 for j1 in V1 for j2 in V2]] 
          for i in I]
    c2 = [
            [[X(i,j1,j2)for i in I for j1 in V1]+[Z(j2,2)], [q[i] for i in I for j1 in V1]+ [-V[1][j2]]]
          for j2 in V2]
    c3 = [
            [[X(i,j1,j2) for i in I for j2 in V2]+[Z(j1,1)], [q[i] for i in I for j2 in V2]+ [-V[0][j1]]]
          for j1 in V1]
    
    s1 = "E" * len(I)
    s2 = "L" * len(V1)
    s3 = "L" * len(V2)
    
    r1 = [1 for i in I]
    r2 = [0 for j2 in V2]
    r3 = [0 for j1 in V1]
    
    rows = c1+c2+c3
    senses = s1+s2+s3
    rhs =  r1+r2+r3
    
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
    Z = solution[I*V1*V2:]

    return prob, X, Z