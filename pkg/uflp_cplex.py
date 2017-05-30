
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
    
    #####################################################################
    # Objective function
    
    Xs = {
        "name" : [],
        "coef" : [],
        "type" : [],
        "ub"   : [],
        "lb"   : [],
    }

    
    variables = [Xs]
    #####################################################################
    # Constraints
    
    c1 = {
        "lin_expr": [[[], []]
                     ],
        "senses"  : [],
        "rhs"     : []
    }
    
    constraints = [c1]
    #####################################################################
    # Solving
    prob = cplex_solve(variables,constraints,
                       minimize=True, path=path, verbose=verbose)

    #####################################################################
    # Extract solution
    solution = prob.solution.get_values()

    return prob