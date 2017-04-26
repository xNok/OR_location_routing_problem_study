
def cflp_first_tsp_second(G,pos, labels, colors, size,
                I,J,C,
                W1,W2,W3,F1,F2,
                U,Q_icp,Q_crc,
                plots=True, expid=""):
    
    from pkg.cflp_cplex import cflp_cplex
    from pkg.tsp_cplex import tsp_cplex
    from pkg.read_problem import read_problem, extract_problem
    from pkg.lrp_nodes_graph import lrp_nodes_graph, lrp_draw_and_save
    import numpy as np
    import pandas as pd
    from IPython.display import display, HTML

    #######################################################################
    # Solve first problem
    prob1, Y1, N_icp = cflp_cplex(I,J,
                W1,F1,U,Q_icp,
                relaxation=False)
    
    #######################################################################
    # Prepare 2nd problem
    H1 = [j for j,vj in enumerate(N_icp) if vj > 0.5]
    
    c2=[];    u2=[];
    for j in H1:
        c2.append(W2[j])
        sqi = 0
        for i in range(I):
            sqi += U[i]*Y1[i][j]
        u2.append(sqi)
    #######################################################################        
    # Solve Second problem
    prob2, Y2, N_crc = cflp_cplex(len(u2),C,
            c2,F2,u2,Q_crc,
            relaxation=False)    
    #######################################################################
    # Preparing TSP
    H2 = [j for j,vj in enumerate(N_crc) if vj > 0.5]
    tY2 = np.transpose(Y2)
    W3 = np.asarray(W3)
    
    #/!\ Use H1 as a labeling array

    S_tsp = [] #set of ICP in each TSP
    for c,vc in enumerate(H2):
        S_tsp.append([H1[j] for j,vj in enumerate(tY2[c]) if vj > 0.5]+[J+vc])
    
    w_tsp = []
    for submat in S_tsp:
        w_tsp.append(W3[submat,:][:,submat])
    #######################################################################
    # Solving TSP
    routes = []
    for c,vc in enumerate(w_tsp):
        prob, X = tsp_cplex(len(vc),vc, relaxation=False)
        # Extract routes
        path = []
        for j,xj in enumerate(X):
            for i,xij in enumerate(xj):
                if xij == 1:
                    path.append((S_tsp[c][i],S_tsp[c][j]))
        routes.append(path)
    #######################################################################
    # Draw solution
    if(plots):
        ###############################
        # DataFrames
        display(pd.DataFrame(N_crc).transpose())
        display(pd.DataFrame(N_icp).transpose())
        for c,vc in enumerate(w_tsp):
            display(pd.DataFrame(path).transpose())   
        ###############################
        # Network
        G2 = G.copy()
        colors = colors[:];size = size[:];
        # ICP-Cus
        for j,vj in enumerate(Y1):
            for i,vi in enumerate(vj):
                if vi == 1:
                    G2.add_edge(I+i,j)
        # ICP
        for j,vj in enumerate(N_icp):
            if vj < 0.5:
                colors[I+j] = "grey"
                labels[I+j] = ""
                size[I+j] = 50
                
        # ICP-CRC
        for j,vj in enumerate(Y2):
            for i,vi in enumerate(vj):
                if vi == 1:
                    G2.add_edge(I+J+i,I+H1[j])
        # CRC
        for j,vj in enumerate(N_crc):
            if vj < 0.5:
                colors[I+J+j] = "grey"
                labels[I+J+j] = ""
                size[I+J+j] = 50
                
        # Routes
        for r,vr in enumerate(routes):
            for c, vc in enumerate(vr):
                G2.add_edge(I+vc[0],I+vc[1])

        lrp_draw_and_save(G2, pos, labels, colors, size, expid+"/cflp_cplex.png")
    
    return Y1, N_icp, N_crc, routes