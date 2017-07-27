
import cplex_solve
import numpy as np

def uflp_cplex(I,J,
            d,f,
            relaxation=False,path=None,verbose=False):
    """
    I,J number of customer and facilities
    d,f cost matrices for variables cost and fixed cost
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
        "coef" : [d[i][j] for i in I for j in J],
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
        "rhs"     : [1 for i in I]
    }
    
    c2 = {
        "lin_expr": [[[X(i,j),Z(j)], [1,-1]]
                     for i in I for j in J],
        "senses"  : ["L" for i in I for j in J],
        "rhs"     : [0 for i in I for j in J]
    }
    
    constraints = [c1, c2]
    #####################################################################
    # Solving
    prob = cplex_solve.from_template(variables,constraints,
                       minimize=True, path=path, verbose=verbose)

    #####################################################################
    # Extract solution
    solution = prob.solution.get_values()
    I = len(I); J = len(J);
    
    X = np.reshape(solution[0:I*J],(I,J))
    Z = solution[I*J:I*J+J]

    return prob, X, Z