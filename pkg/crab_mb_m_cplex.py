
from pkg.cplex_solve import cplex_solve
import numpy as np              # mathematic tools library
import networkx as nx           # network representation library
import cplex

def crab_mb_m_cplex(I,J,C,B,K,V,
            w,Dcj,FCV,FCT,FCR,Dc,q,
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
            w, Dcj, Dc cost related to traveling distances cus-ICP, ICP-CRC, CRC-PC
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
    
    def Z(i,j,c):
        return "Z_" + str(i) + "_" + str(j) + "_" + str(c)
    
    def Nj(j):
        return "Nj_" + str(j)
    
    def Nc(c):
        return "Nc_" + str(c)
    
    def V(j):
        return "V_" + str(j)
    
    def VZ(c,j,b):
        return "VZ_" + str(c) + "_" + str(j) + "_" + str(b)

    CuJ = range(C+J); iJ = range(C,C+J,1)
    I = range(I); J = range(J); B = range(B); C = range(C);
    
    #####################################################################
    # Objective function
    objy = [w[i][j]  for i in I for j in J]
    objz = [Dcj[c][j]+FCV[b] for c in CuJ for j in CuJ for b in B]
    objn = [FCT[j] for j in J] + [FCR[c]+Dc[c] for c in C]
    
    ## variables names
    Ys = [Y(i,j)  for i in I for j in J]
    Zs = [Z(c,j,b) for c in CuJ for j in CuJ for b in B]
    Ns = [Nj(j) for j in J] + [Nc(c) for c in C]
    
    # Dummy variables
    Vs = [V(j) for j in J]; objv = [0 for j in J]
    VZs = [VZ(c,j,b) for c in CuJ for j in CuJ for b in B]
    objvz = [0 for c in CuJ for j in CuJ for b in B]

    ## Objective function sum aggregation
    obj = objy + objz + objn + objv + objvz
    colnames = Ys + Zs + Ns + Vs + VZs
    if relaxation: #Integrality constraint
        types    = "C" * len(colnames) 
    else: #Integrality constraint
        types    = "I" * (len(Ys)+len(Zs)+len(Ns)) + "C" * (len(Vs)+len(VZs))

    #####################################################################
    # Constraints
    
    # Ys FLP constraints
    c2 = [
            [[Y(i,j) for j in J], [1 for j in J]] 
          for i in I]
    c4 = [
            [[Y(i,j) for i in I]+[Nj(j)], [q[i] for i in I]+[-Q[0][j]]] 
          for j in J]
    c5 = [
            [[Y(i,j) for i in I]+[V(j)], [q[i] for i in I]+[-1]] 
          for j in J]

    s2 = "E" * len(I)
    s4 = "L" * len(J)

    r2 = [1 for i in I]
    r4 = [0 for j in J]
    
    # Zs FLP constraints
    c6 = [
            [[Z(c,j,b) for c in C for b in B], [1 for c in C for b in B]] 
        for j in iJ]
    c11 = [
            [[Z(c,j,b) for c in C for j in iJ], [1 for c in C for j in iJ]] 
        for b in B]
    c12 = [
            [[VZ(c,j,b) for j in iJ for c in CuJ], [1 for j in iJ for c in CuJ]] 
        for b in B]
    
    s5  = "E" * len(J)
    s6  = "E" * len(J)
    s11 = "L" * len(B)
    s12 = "L" * len(B)
    
    r5  = [1 for j in J]
    r6  = [1 for j in J]
    r11 = [1 for b in B]
    r12 = [Q[1][b] for b in B]
    
    # Zs VRP constraints
    rows   = c2+c4
    senses = s2+s4
    rhs    = r2+r4
    
    #####################################################################
    # Bounds
    ub = [1 for i in range(len(Ys)+len(Zs)+len(Ns))] + \
        [cplex.infinity for i in range(len(Vs)+len(VZs))]
    lb = [0 for i in range(len(Ys)+len(Zs)+len(Ns))] + \
        [0 for i in range(len(Vs)+len(VZs))]
    
    #####################################################################
    # Solving
    prob = cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=path)

    #####################################################################
    # Extract solution
    CuJ = len(C)+len(J); I = len(I); J = len(J); B = len(B); C = len(C);
    
    solution = prob.solution.get_values()
    Y = np.reshape(solution[0:len(Ys)],(I,J))
    Z = np.reshape(solution[len(Ys):len(Ys)+len(Zs)],(CuJ,CuJ,B))
    N = solution[len(Ys)+len(Zs):len(Ys)+len(Zs)+len(Ns)]
    V = solution[len(Ys)+len(Zs)+len(Ns):]

    return prob, Y, Z, N, V