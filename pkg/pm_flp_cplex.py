
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library
from pkg.cplex_solve import cplex_solve

def pm_flp_cplex(I,J,
            c,p,
            relaxation=False,path=None):
    #####################################################################
    # Decision variables
    
    def X(i,j):
        return "X_" + str(i) + "_" + str(j)

    def Z(j):
        return "Z_" + str(j)

    #####################################################################
    # Objective function
    
    obj1 = [c[i][j]  for i in range(I) for j in range(J)]
    obj2 = [0 for j in range(J)]
    
    ## variables name
    Xs = [X(i,j) for i in range(I) for j in range(J)]
    Zs = [Z(j) for j in range(J)]

    ## Objective function sum aggregation
    obj = obj1 + obj2
    colnames = Xs + Zs
    if relaxation:
        types    = "C" * (I*J+J) #Integrality constraint
    else:
        types    = "I" * (I*J+J) #Integrality constraint

    #####################################################################
    # Constraints
    
    c1 = [[[X(i,j) for j in range(J)], [1 for j in range(J)]] for i in range(I)]
    c2 = [[[X(i,j),Z(j)], [1,-1]] for i in range(I) for j in range(J)]
    c3 = [[[Z(j) for j in range(J)], [1 for j in range(J)]]]
    
    s1 = "E" * I
    s2 = "L" * (I*J)
    s3 = "E"
    
    r1 = [1 for i in range(I)]
    r2 = [0 for i in range(I) for j in range(J)]
    r3 = [p]
    
    rows   =   c1+c2+c3
    senses =   s1+s2+s3
    rhs    =   r1+r2+r3
    
    #####################################################################
    # Bounds
    ub = [1 for i in range(I*J+J)]
    lb = [0 for i in range(I*J+J)]
    
    #####################################################################
    # Solving
    prob = cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=path)

    #####################################################################
    # Extract solution
    solution = prob.solution.get_values()
    X = np.reshape(solution[0:I*J],(I,J))
    Z = solution[I*J:I*J+J]

    return prob, X, Z