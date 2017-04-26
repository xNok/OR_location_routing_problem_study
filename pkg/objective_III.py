
def objective_III(Y,routes,Nj,Nc,
                    I,J,C,B,
                   w,DjUc,Dc,FCV,FCT,FCR):
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
    for b,r in enumerate(routes):
        for l in r:
            c = l[0]; j = l[1];
            sum2_2 += DjUc[c][j]
                
    sum2_3 = 0
    for j in range(J):
        sum2_3 += FCT[j] * Nj[j]
        
    sum2_4 = 0
    for c in range(C):
        sum2_4 += (FCR[c] + Dc[c]+ FCV[c]) * Nc[c]
      
    return sum2_1+sum2_2+sum2_3+sum2_4, sum2_1, sum2_2, sum2_3, sum2_4