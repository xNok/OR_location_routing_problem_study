
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library
from pkg.cplex_solve import cplex_solve
import cplex

def vrp_2_t_cplex(I,J,B,
            c,f,
            relaxation=False,path=None):

    #####################################################################
    # Decision variables
    
    def X(i,j,b):
        return "X_" + str(i) + "_" + str(j) + "_" + str(b)
    def U(i):
        return "U_" + str(i)
    def N(j):
        return "N_" + str(j)
    
    IuJ = range(I+J); J = range(I,I+J,1)
    I = range(I); B = range(B); 
    #####################################################################
    # Objective function
    Xs = {
        "name" : [X(i,j,b) for i in IuJ for j in IuJ for b in B],
        "coef" : [c[i][j] for i in IuJ for j in IuJ for b in B],
        "type" : ["I" for i in IuJ for j in IuJ for b in B],
        "ub"   : [1 for i in IuJ for j in IuJ for b in B],
        "lb"   : [0 for i in IuJ for j in IuJ for b in B],
    }
    Ns = {
        "name" : [N(j) for j in J],
        "coef" : [f[j-len(I)] for j in J],
        "type" : ["I" for j in J],
        "ub"   : [1 for j in J],
        "lb"   : [0 for j in J],
    }
    Us = {
        "name" : [U(i) for i in IuJ],
        "coef" : [0 for i in IuJ],
        "type" : ["C" for i in IuJ],
        "ub"   : [cplex.infinity for i in IuJ],
        "lb"   : [0 for i in IuJ],
    }

    Variables = [Xs,Ns,Us]
    ## Objective function sum aggregation
    obj = [];ub = [];lb = [];colnames = [];types = [];
    for v in Variables:
        obj      = obj + v["coef"]
        ub       = ub  + v["ub"]
        lb       = lb  + v["lb"]
        colnames = colnames + v["name"]
        types    = types + v["type"]

    #####################################################################
    # Constraints
    c0 = {
        "lin_expr": [[[X(i,i,b) for i in IuJ for b in B],
                      [1 for i in IuJ for b in B]] 
        ],
        "senses"  : ["E"],
        "rhs"     : [0]
    }
    c1 = {
        "lin_expr": [[[X(i,j,b) for b in B for j in IuJ],
                      [1 for b in B for j in IuJ]] 
         for i in I],
        "senses"  : ["E" for i in I],
        "rhs"     : [1 for i in I]
    }
    c2 = {
        "lin_expr": [[[X(i,j,b) for i in IuJ if i!=j]+[X(j,i,b) for i in IuJ if i!=j], 
             [1 for i in IuJ if i!=j]+[-1 for i in IuJ if i!=j]] 
        for j in IuJ for b in B],
        "senses"  : ["E" for j in IuJ for b in B],
        "rhs"     : [0 for j in IuJ for b in B]
    }
    c3 = {
        "lin_expr": [[[X(i,j,b) for i in IuJ for j in J],
                      [1 for i in IuJ for j in J]] 
        for b in B],
        "senses"  : ["L" for b in B],
        "rhs"     : [1 for b in B]
    }
    c4 = {
        "lin_expr": [[[U(i),U(j)]+[X(i,j,b) for b in B],
                      [1,-1]+[len(I)+len(J) for b in B]] 
        for i in IuJ for j in IuJ if i!=j],
        "senses"  : ["L" for i in IuJ for j in IuJ if i!=j],
        "rhs"     : [len(I)+len(J)-1 for i in IuJ for j in IuJ if i!=j]
    }

    # Zs VRP constraints
    Constraints = [c0,c1,c2,c3,c4]
    rows = []; senses = []; rhs = [];
    for c in Constraints:
        rows   = rows   + c["lin_expr"]
        senses = senses + c["senses"]
        rhs    = rhs    + c["rhs"]

    print(len(rows),len(senses),len(rhs))
    
    #####################################################################
    # Solving
    prob = cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=path)

    #####################################################################
    # Extract solution
    IuJ = len(I)+len(J); J = len(J)
    I = len(I); B = len(B); 
    
    solution = prob.solution.get_values()
    X = np.reshape(solution[0:IuJ*IuJ*B],(IuJ,IuJ,B))
    N = solution[IuJ*IuJ*B:IuJ*IuJ*B]

    return prob, X, N