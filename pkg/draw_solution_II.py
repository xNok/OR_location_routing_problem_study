
def draw_solution_II(I,J,C,
                    N_crc, N_icp,
                    Y1,Y2, routes, expid,
                    G, pos, labels, colors, size, path=None):
    
    from IPython.display import display, HTML
    import pandas as pd
    from pkg.draw_solution_II import draw_solution_II
    from pkg.lrp_nodes_graph import lrp_nodes_graph, lrp_draw_and_save
    
    H1 = [j for j,vj in enumerate(N_icp) if vj > 0.5]
    
    ###############################
    # DataFrames
    display(pd.DataFrame(N_crc).transpose())
    display(pd.DataFrame(N_icp).transpose())
    display(pd.DataFrame(routes).transpose())   
    ###############################
    # Network
    G2 = G.copy()
    colors = colors[:];size = size[:]; labels = labels.copy()
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

    lrp_draw_and_save(G2, pos, labels, colors, size, path)
    
    return G2