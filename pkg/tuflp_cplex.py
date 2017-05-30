
from pkg.cplex_solve import cplex_solve
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library

def tuflp_cplex(I,V1,V2,
            c,f,
            relaxation=False,path=None,verbose=False):
    """
    I,V1,V2 number of customers, level 1 facility, level 2 facility
    c,f cost matrix for connection and setup
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
    
    Xs = {
        "name" : [X(i,j) for i in I for j1 in V1 for j2 in V2],
        "coef" : [c[i][j1][j2] for i in I for j1 in V1 for j2 in V2],
        "type" : ["C" if relaxation else "I" for i in I for j1 in V1 for j2 in V2],
        "ub"   : [1 for i in I for j1 in V1 for j2 in V2],
        "lb"   : [0 for i in I for j1 in V1 for j2 in V2],
    }
    
    Zs = {
        "name" : [Z(j) for j in range(len(V1)+len(V2))],
        "coef" : [f[j] for j in range(len(V1)+len(V2))],
        "type" : ["C" if relaxation else "I" for j in range(len(V1)+len(V2))],
        "ub"   : [1 for j in range(len(V1)+len(V2))],
        "lb"   : [0 for j in range(len(V1)+len(V2))],
    }

    #####################################################################
    # Constraints
    
    c1 = {
        "lin_expr": [[[X(i,j1,j2) for j1 in V1 for j2 in V2], [1 for j1 in V1 for j2 in V2]] 
          for i in range(I)],
        "senses"  : ["E" for i in range(I)],
        "rhs"     : [0 for i in range(I)]
    }
    
    c2 = {
        "lin_expr": [[[X(i,j1,j2) for j1 in V1]+[Z(j2,2)], [1 for j1 in V1]+ [-1]]
          for i in I for j2 in V2],
        "senses"  : ["L" for i in I for j2 in V2],
        "rhs"     : [0 for i in I for j2 in V2]
    }
    
    c3 = {
        "lin_expr": [[[X(i,j1,j2) for j2 in V2]+[Z(j1,1)], [1 for j2 in V2]+ [-1]]
          for i in I for j1 in V1],
        "senses"  : ["L" for i in I for j1 in V1],
        "rhs"     : [0 for i in I for j1 in V1]
    }
    
    constraints = [c1, c2, c3]

    #####################################################################
    # Solving
    prob = cplex_solve(variables,constraints,
                       minimize=True, path=path, verbose=verbose)
    #####################################################################
    # Extract solution
    I = len(I); V1 = len(V1); V2 = len(V2);
    solution = prob.solution.get_values()
    X = np.reshape(solution[0:I*V1*V2],(I,V1,V2))
    Z = solution[I*V1*V2:]

    return prob, X, Z