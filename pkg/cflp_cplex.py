
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library
from pkg.cplex_solve import cplex_solve

def cflp_cplex(I,J,
            c,f,
            q,V,
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
    obj2 = [f[j] for j in range(J)]
    
    ## variables name
    Ys = [ X(i,j) for i in range(I) for j in range(J)]
    N_icps = [Z(j) for j in range(J)]

    ## Objective function sum aggregation
    obj = obj1 + obj2
    colnames = Ys + N_icps
    if relaxation:
        types    = "C" * (I*J+J) #Integrality constraint
    else:
        types    = "I" * (I*J+J) #Integrality constraint

    #####################################################################
    # Constraints
    
    c1 = [
        [[X(i,j) for j in range(J)], [1 for j in range(J)]]
        for i in range(I)]
    c2 = [
        [[X(i,j) for i in range(J)]+[Z(j)], [q[i] for i in range(J)]+[-V[j]]] 
        for j in range(J)]
    
    s1 = "E" * I
    s2 = "L" * J
    
    r1 = [1 for i in range(I)]
    r2 = [0 for i in range(J)]
    
    rows = c1+c2
    senses = s1+s2
    rhs =  r1+r2
    
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
    Y = np.reshape(solution[0:I*J],(I,J))
    N_icp = solution[I*J:I*J+J]

    return prob, Y, N_icp