
import cplex
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library

def flp_cplex(I,J,C,
            W,FCT,FCR,D,
            relaxation=False,path=None):

    #####################################################################
    # Objective function
    
    obj1 = [W[i][j]  for i in range(I) for j in range(J)]
    objx = [D[j][c]  for j in range(J) for c in range(C)]
    obj2 = [FCT[j][0] for j in range(J)]
    obj5 = [FCT[c][0] for c in range(C)]
    

    ## variablesnames
    Ys = [ "Y_" + str(i) + "_" + str(j) for i in range(I) for j in range(J)]
    Xs = [ "X_" + str(j) + "_" + str(c) for j in range(J) for c in range(C)]
    N_icps = ["N_icp_" + str(j) for j in range(J)]
    N_crcs = ["N_crc_" + str(c) for c in range(C)]

    ## Objective function sum aggregation
    obj = obj1 + obj2 + obj5 + objx
    colnames = Ys + Xs + N_icps + N_crcs
    if relaxation:
        types    = "C" * (I*J+J*C+J+C) #Integrality constraint
    else:
        types    = "I" * (I*J+J*C+J+C) #Integrality constraint

    #####################################################################
    # Constraints
    
    c1 = [[["Y_" + str(i) + "_" + str(j) for i in range(I)], [1 for i in range(I)]] for j in range(J)]
    c2 = [[["X_" + str(j) + "_" + str(c) for j in range(J)], [1 for j in range(J)]] for c in range(C)]
    C3 = [[["Y_" + str(i) + "_" + str(j),"N_icp_" + str(j)], [1,-1]] for i in range(I) for j in range(J)]
    C4 = [[["X_" + str(j) + "_" + str(c),"N_crc_" + str(c)], [1,-1]] for j in range(J) for c in range(C)]
    
    s1 = "E" * J
    s2 = "L" * C 
    s3 = "E" * (I*J)
    s4 = "L" * (J*C)
    
    r1 = [1 for j in range(J) ]
    r2 = [1 for j in range(C) ]
    r3 = [0 for i in range(I) for j in range(J)]
    r4 = [0 for j in range(J) for c in range(C)]
    
    rows = c1+c2+c3+c4
    senses = s1+s2+s3+s4
    rhs =  r1+r2+r3+r4
    
    #####################################################################
    # Bounds
    ub = [1 for i in range(I*J+J*C+J+C)]
    lb = [0 for i in range(I*J+J*C+J+C)]

    #####################################################################
    # Creating problem

    prob = cplex.Cplex()
    ## Objective function sense
    prob.objective.set_sense(prob.objective.sense.minimize)
    ## Objective function
    prob.variables.add(obj=obj,ub=ub,lb=lb,names=colnames,types=types)
    ## Constraintes
    prob.linear_constraints.add(lin_expr=rows,senses=senses, rhs=rhs)

    #####################################################################
    # Saving the linear problem formulation into a file
    if path:
        prob.write(path) # print the formulation into a file

    #####################################################################
    # Solving problem
    prob.solve()

    #####################################################################
    # Extract solution
    X = np.reshape(prob.solution.get_values()[num_f:],(num_c,num_f))
    Z = prob.solution.get_values()[:num_f]

    return prob, X, Z