
def crab_mb_m(I,J,C,B,K,V,
            w,Dcj,FCV,FCT,FCR,Dc,q,
            Q):
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
        return "X_" + str(i) + "_" + str(j1)
    
    def Z(i,j,jc):
        return "T_" + str(i) + "_" + str(j) + "_" + str(c)
    
    def Nj(j):
        return "Nj_" + str(j)
    
    def Nc(c):
        return "Nc_" + str(c)

    CuJ = range(C+J); I = range(I); J = range(J); B = range(B);
    
    #####################################################################
    # Objective function
    
    objy = [w[i][j]  for i in I for j in J]
    objz = [Dcj[c][j]+FCV[b] for c in CuJ for j in CuJ for b in b]
    objn = [FCT[j] for j in J] + [FCR[c]+D[c] for c in c]

    ## variables names
    Ys = [Y(i,j)  for i in I for j in J]
    Zs = [Z(c,j,b) for c in C for j in J for b in b]
    Ns = [Nj(j) for j in J] + [Nc(c) for c in c]

    ## Objective function sum aggregation
    obj = objy + objz + objn
    colnames = Ys + Zs + Ns
    if relaxation:
        types    = "C" * (len(Ys)+len(Zs)+len(Ns)) #Integrality constraint
    else:
        types    = "I" * (len(Ys)+len(Zs)+len(Ns)) #Integrality constraint

    #####################################################################
    # Constraints
    
    # Ys FLP constraints
    c1 = [
            [[Y(i,j) for j in J], [1 for j in J]] 
          for i in I]
    c3 = [
        [[Y(i,j) for j in J], [1 for j in J]] 
      for i in I]

    s1 = "E" * len(I)
    c3 = "L" * len(I)

    r1 = [1 for i in I]
    r3 = [Q[i] for i in I]
    
    # Zs FLP constraints
    
    # Zs VRP constraints

    rows = c1+c3
    senses = s1+s3
    rhs =  r1+r3
    
    #####################################################################
    # Bounds
    ub = [1 for i in range(len(Ys)+len(Zs)+len(Ns))]
    lb = [0 for i in range(len(Ys)+len(Zs)+len(Ns))]

    #####################################################################
    # Solving
    prob = cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=path)

    #####################################################################
    # Extract solution
    CuJ = len(C)+len(J); I = len(I); J = len(J); B = len(B);
    
    solution = prob.solution.get_values()
    Y = np.reshape(solution[0:I*J],(I,J))
    Z = np.reshape(solution[I*J:I*J+CuJ*CuJ*B],(CuJ,CuJ,B))
    N = solution[I*J+CuJ*CuJ*B:]

    return prob, Y, Z, N