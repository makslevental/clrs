import random

import networkx as nx


def edmondskarp(G):
    pass

if __name__ == '__main__':
    G = nx.fast_gnp_random_graph(10,.3,directed=True)
    while not nx.is_directed_acyclic_graph(G):
        G = nx.fast_gnp_random_graph(10,.3,directed=True)

    pos = nx.spring_layout(G)

    for u,v in G.edges_iter():
        G.edge[u][v]['weight'] = random.random()