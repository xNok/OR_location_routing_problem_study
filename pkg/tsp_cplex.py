
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library
from pkg.cplex_solve import cplex_solve
import cplex

def tsp_cplex(N,
            c,
            relaxation=False,path=None):

    #####################################################################
    # Decision variables
    
    def X(i,j):
        return "X_" + str(i) + "_" + str(j)
    
    def U(i):
        return "U_" + str(i)
    
    N = range(N);
    #####################################################################
    # Objective function
    
    obj1 = [c[i][j] for i in N for j in N]
    obj2 = [0 for i in N]
    
    ## variables name
    Xs = [X(i,j) for i in N for j in N]
    Us = [U(i) for i in N]

    ## Objective function sum aggregation
    obj = obj1 + obj2
    colnames = Xs + Us
    if relaxation:
        types    = "C" * (len(Xs)+len(Us)) #Integrality constraint
    else:
        types    = "I" * len(Xs) + "C" * len(Us) #Integrality constraint

    #####################################################################
    # Constraints
    
    c1 = [
            [[X(i,j) for i in N if i != j], [1 for i in N if i != j]]
        for j in N]
    
    c2 = [
            [[X(i,j) for j in N if i != j], [1 for j in N if i != j]]
        for i in N]
    
    subtours = [(i,j) for i in N for j in N if i != j and j > 0 and i > 0]
    
    c3 = [
            [[U(i),U(j),X(i,j)], [1,-1,len(N)-1]]
        for i,j in subtours]
    
    s1 = "E" * len(N)
    s2 = "E" * len(N)
    s3 = "L" * len(subtours)

    r1 = [1 for i in N]
    r2 = [1 for i in N]
    r3 = [len(N)-2 for i in range(len(subtours))]

    rows = c1+c2+c3
    senses = s1+s2+s3
    rhs =  r1+r2+r3
    
    #####################################################################
    # Bounds
    ub = [1 for i in range(len(Xs))] + [cplex.infinity for i in range(len(Us))]
    lb = [0 for i in range((len(Xs)+len(Us)))]
    
    #####################################################################
    # Solving
    prob = cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=path)

    #####################################################################
    # Extract solution
    N = len(N)
    
    solution = prob.solution.get_values()
    X = np.reshape(solution[0:N*N],(N,N))

    return prob, X