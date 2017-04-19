import networkx as nx
import matplotlib.pyplot as plt

def lrp_nodes_graph(xy_customers, xy_icps, xy_crcs, xy_pc):
    G = nx.Graph()
    colors=[]
    pos=[]
    labels={}
    size=[]
    
    num_cus = len(xy_customers)
    num_icps = len(xy_icps)
    num_crcs  = len(xy_crcs)

    for i, val in enumerate(xy_customers):
        G.add_node(i)
        pos.append((val[0],val[1]))
        colors.append("blue")
        labels[i]=""
        size.append(100)

    for i, val in enumerate(xy_icps):
        G.add_node(i+num_cus)
        pos.append((val[0],val[1]))
        colors.append("red")
        labels[i+num_cus]="icp"+str(i)
        size.append(200)

    for i, val in enumerate(xy_crcs):
        G.add_node(i+num_cus+num_icps)
        pos.append((val[0],val[1]))
        colors.append("green")
        labels[i+num_cus+num_icps]="crc"+str(i)
        size.append(300)
        
    G.add_node(num_cus+num_icps+num_crcs)
    pos.append((xy_pc[0],xy_pc[1]))
    colors.append("orange")
    labels[num_cus+num_icps+num_crcs]="pc"
    size.append(300)
        
    return G, pos, labels, colors, size

def lrp_draw_and_save(G, pos, labels, colors, size, path):
    plt.grid('on')
    nx.draw_networkx(G,pos,labels=labels,node_color=colors,with_labels=True, node_size=size)
    plt.savefig(path, format="PNG")