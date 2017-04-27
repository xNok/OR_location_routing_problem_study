
from pkg.cplex_solve import cplex_solve
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library
import cplex

def crab_mb_m_cplex(I,J,C,B,K,V,
            w,Djc,FCV,FCT,FCR,Dc,q,
            Q,relaxation=False,path=None):
    """
    Parameters:
        Sets:
            I,J,C,K,V,B -> customer, ICPs, CRCs, qualities, varieties, vehicles
        Costs:
            FCT, FCR, FCV, fixed cost for ICP, CRC, vehicle
            IP, PC acquisition and processiong cost
         Weight:
            q, nbr unit collected
            w, Djc, Dc cost related to traveling distances cus-ICP, ICP-CRC, CRC-PC
        Capacity:
            Q capacity matrix
     
     Decision Vqriables:
        Y_ij customer i associated to ICP j
        Z_cjb vehicle travel from CRC_c to ICP_j on route b
        N_icp, N_crc -> ICP / CRC is open
    """
    #####################################################################
    # Decision variables
    
    def Y(i,j):
        return "Y_" + str(i) + "_" + str(j)
    
    def Z(c,j,b):
        return "Z_" + str(c) + "_" + str(j) + "_" + str(b)
    
    def N(j):
        return "N_" + str(j)
    
    def V(j):
        return "V_" + str(j)
    
    def VZ(c,j,b):
        return "VZ_" + str(c) + "_" + str(j) + "_" + str(b)
    
    def U(j):
        return "L_" + str(j)

    CuJ = range(C+J); C = range(J,C+J,1)
    I = range(I);J = range(J); B = range(B); 
    
    #####################################################################
    ## variables
    Ys = {
        "name" : [Y(i,j)  for i in I for j in J],
        "coef" : [w[i][j]  for i in I for j in J],
        "type" : ["I"  for i in I for j in J],
        "ub"   : [1  for i in I for j in J],
        "lb"   : [0  for i in I for j in J],
    }
    Zs = {
        "name" : [Z(c,j,b) for c in CuJ for j in CuJ for b in B],
        "coef" : [Djc[c][j] for c in CuJ for j in CuJ for b in B],
        "type" : ["I" for c in CuJ for j in CuJ for b in B],
        "ub"   : [1 for c in CuJ for j in CuJ for b in B],
        "lb"   : [0 for c in CuJ for j in CuJ for b in B],
    }
    Ns = {
        "name" : [N(j) for j in J] + [N(c) for c in C],
        "coef" : [FCT[j] for j in J] + [FCR[c-len(J)]+Dc[c-len(J)]+FCV[c-len(J)] for c in C],
        "type" : ["I" for j in J] + ["I" for c in C],
        "ub"   : [1 for j in J] + [1 for c in C],
        "lb"   : [0 for j in J] + [0 for c in C],
    }
    # Dummy variables
    Vs = {
        "name" : [V(j) for j in J],
        "coef" : [0  for j in J],
        "type" : ["C"  for j in J],
        "ub"   : [cplex.infinity  for j in J],
        "lb"   : [0  for j in J],
    }
    VZs = {
        "name" : [VZ(c,j,b) for c in CuJ for j in CuJ for b in B],
        "coef" : [0 for c in CuJ for j in CuJ for b in B],
        "type" : ["C" for c in CuJ for j in CuJ for b in B],
        "ub"   : [cplex.infinity for c in CuJ for j in CuJ for b in B],
        "lb"   : [0 for c in CuJ for j in CuJ for b in B],
    }
    Us = {
        "name" : [U(j) for j in CuJ],
        "coef" : [0 for j in CuJ],
        "type" : ["C" for j in CuJ],
        "ub"   : [cplex.infinity for j in CuJ],
        "lb"   : [0 for j in CuJ],
    }

    Variables = [Ys,Zs,Ns,Vs,Us]
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
    
    # Ys FLP constraints
    c2 = {
        "lin_expr": [[[Y(i,j) for j in J]
                       ,[1 for j in J]] 
          for i in I],
        "senses"  : ["E" for i in I],
        "rhs"     : [1 for i in I]
    }
    c4 = {
        "lin_expr": [[[Y(i,j) for i in I]+[N(j)],
                      [q[i] for i in I]+[-Q[0][j]]] 
          for j in J],
        "senses"  : ["L" for j in J],
        "rhs"     : [0 for j in J]
    }
    c5 = {
        "lin_expr": [[[Y(i,j) for i in I]+[V(j)]
                      , [q[i] for i in I]+[-1]] 
          for j in J],
        "senses"  : ["E" for j in J],
        "rhs"     : [0 for j in J]
    }

    # Zs FLP constraints
    cstar = {
        "lin_expr": [[[Z(c,c,b) for c in CuJ for b in B],
                      [1 for c in CuJ for b in B]] 
        ],
        "senses"  : ["E"],
        "rhs"     : [0]
    }
    c6 = {
        "lin_expr": [[[Z(j,c,b) for c in CuJ for b in B]+[N(j)],
                      [1 for c in CuJ for b in B]+[-1]] 
         for j in J],
        "senses"  : ["E" for j in J],
        "rhs"     : [0 for j in J]
    }
    c8 = {
        "lin_expr": [[[Z(c,j,b) for j in J for b in B]+[N(c)],
                      [1 for j in J for b in B]+[-1]] 
         for c in C],
        "senses"  : ["E" for c in C],
        "rhs"     : [0 for c in C]
    }
    c11 = {
        "lin_expr": [[[Z(c,j,b) for c in C for j in CuJ],
                      [1 for c in C for j in CuJ]] 
        for b in B],
        "senses"  : ["L" for b in B],
        "rhs"     : [1 for b in B]
    }
    c12 = {
        "lin_expr": [[[VZ(c,j,b) for c in CuJ for j in J],
                      [1 for c in CuJ for j in J]] 
        for b in B],
        "senses"  : ["L" for c in CuJ],
        "rhs"     : [Q[1][b] for b in B]
    }
    c13 = {
        "lin_expr": [[[U(c),U(j)]+[Z(c,j,b) for b in B],
                      [1,-1]+[len(J)+len(C) for b in B]] 
        for c in J for j in J if c!=j],
        "senses"  : ["L" for c in J for j in J if c!=j],
        "rhs"     : [len(J)+len(C)-1 for c in J for j in J if c!=j]
    }
    c14 = {
        "lin_expr": [[[Z(c,j,b) for c in CuJ if c!=j]+[Z(j,c,b) for c in CuJ if c!=j], 
             [1 for c in CuJ if c!=j]+[-1 for c in CuJ if c!=j]] 
        for j in CuJ for b in B],
        "senses"  : ["E" for j in CuJ for b in B],
        "rhs"     : [0 for j in CuJ for b in B]
    }
    
    # Zs VRP constraints
    
    Constraints = [c2,c4,c5,cstar,c6,c14,c13,c11]
    rows = []; senses = []; rhs = [];
    for c in Constraints:
        rows   = rows   + c["lin_expr"]
        senses = senses + c["senses"]
        rhs    = rhs    + c["rhs"]

    print(len(rows),len(senses),len(rhs))   
        
    #####################################################################
    # Solving
    prob = cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=path, verbose=True)
    
    #####################################################################
    # Extract solution
    CuJ = len(C)+len(J); I = len(I); J = len(J); B = len(B); C = len(C);
    
    solution = prob.solution.get_values()
    Y = np.reshape(solution[0:I*J],(I,J))
    Z = np.reshape(solution[I*J:I*J+CuJ*CuJ*B],(CuJ,CuJ,B))
    N = solution[I*J+CuJ*CuJ*B:I*J+CuJ*CuJ*B+J+C]
    V = solution[I*J+CuJ*CuJ*B+J+C:I*J+CuJ*CuJ*B+J+C+J]

    return prob, Y, Z, N, V