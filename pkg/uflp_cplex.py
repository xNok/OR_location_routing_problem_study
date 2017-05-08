
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library
from pkg.cplex_solve import cplex_solve

def uflp_cplex(I,J,
            v,f,
            relaxation=False,path=None,verbose=False):
    """
    I,J number of customer and facilities
    v,f cost matrices for variables cost and fixed cost
    """
    #####################################################################
    # Decision variables
    
    def X(i,j):
        return "X_" + str(i) + "_" + str(j)

    def Z(j):
        return "Z_" + str(j)
    
    I = range(I); J = range(J);
    #####################################################################
    # Objective function
    
    Xs = {
        "name" : [X(i,j) for i in I for j in J],
        "coef" : [c[i][j] for i in I for j in J],
        "type" : ["C" if relaxation else "I" for i in I for j in J],
        "ub"   : [1 for i in I for j in J],
        "lb"   : [0 for i in I for j in J],
    }
    
    Zs = {
        "name" : [Z(j) for j in J],
        "coef" : [f[j] for j in J],
        "type" : ["C" if relaxation else "I" for j in J],
        "ub"   : [1 for j in J],
        "lb"   : [0 for j in J],
    }
    
    variables = [Xs, Zs]
    #####################################################################
    # Constraints
    
    c1 = {
        "lin_expr": [[[X(i,j) for j in J], [1 for j in J]]
                     for i in I],
        "senses"  : ["E" for i in I],
        "rhs"     : [0 for i in I]
    }
    
    c1 = {
        "lin_expr": [[[X(i,j),Z(j)], [1,-1]]
                     for i in range(I) for j in range(J)],
        "senses"  : ["E" for i in range(I) for j in range(J)],
        "rhs"     : [0 for i in range(I) for j in range(J)]
    }
    
    constraints = [c1, c2]
    #####################################################################
    # Solving
    prob = cplex_solve(variables,constraints,
                       minimize=True, path=path, verbose=verbose)

    #####################################################################
    # Extract solution
    solution = prob.solution.get_values()
    I = len(I); J = len(J);
    
    X = np.reshape(solution[0:I*J],(I,J))
    Z = solution[I*J:I*J+J]

    return prob, X, Z