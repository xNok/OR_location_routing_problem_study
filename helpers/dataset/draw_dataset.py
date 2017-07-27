
import networkx as nx

def draw_dataset(datasets):
    """
    Draw a dot plot of the given dataset
    """
    G = nx.Graph()
    nbr_nodes = 0

    for dataset in datasets:
        d = datasets[dataset]

        for i,xy in enumerate(d["coordinate"]):
            G.add_node(i+nbr_nodes,
               pos=xy,color=d["metadata"]["color"][i],
               size=d["metadata"]["size"][i])

        nbr_nodes += d["number"]

    # Prepare drawing
    pos    = nx.get_node_attributes(G,'pos')
    colors = list(nx.get_node_attributes(G,'color').values())
    size   = list(nx.get_node_attributes(G,'size').values())

    # Draw
    nx.draw_networkx(
        G,pos, node_color=colors,
        node_size=size, with_labels=False
    )
    
    return G