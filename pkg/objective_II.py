
def objective_II(Y,Z,Nj,Nc,
                    I,J,C,B,K,V,
                   w,Dcj,FCV,FCT,FCR,Dc,q,PC,IP):
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
     
     Decision Vqriables:
        Y_ij customer i associated to ICP j
        Z_cjb vehicle travel from CRC_c to ICP_j on route b
        N_icp, N_crc -> ICP / CRC i is open
    """
    sum2_1 = 0
    for i in range(I):
        for j in range(J):
            sum2_1 += w[i][j] * Y[i][j]
    
    sum2_2 = 0
    for c in range(C+J):
        for j in range(C+J):
            for b in range(B):
                sum2_2 += (Dcj[c][j]) * Z[c][j][b]
                
    sum2_3 = 0
    for j in range(J):
        sum2_3 += FCT[j] * N[j]
        
    sum2_4 = 0
    for c in range(C):
        sum2_4 += (FCT[c] + Dc[c] + FCV[c]) * N[c]
      
    return sum2_1+sum2_2+sum2_3+sum2_4, sum2_1, sum2_2, sum2_3, sum2_4