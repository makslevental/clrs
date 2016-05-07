import random
from operator import itemgetter

import networkx as nx


def isthereapath(G,s,t):
    bfs = nx.bfs_tree(G,s)
    path = []
    pred = bfs.predecessors(t)[0] if t in bfs.pred else None
    while pred and (pred != 0):
        path.append(pred)
        pred = bfs.predecessors(pred)[0] if pred in bfs.pred else None



    return list(reversed(list(zip(path+[s],[t]+path))))


def edmondskarp(G: nx.Graph, s, t):

    RG = G.copy()

    for u,v in G.edges_iter():
        G.edge[u][v]['flow'] = 0

    path = isthereapath(RG,s,t)
    while len(path) > 0:
        path_cp = min([RG[u][v]['capacity'] for u,v in path])
        for u,v in path:
            if G.has_edge(u,v):
                G.edge[u][v]['flow'] += path_cp
                RG.edge[u][v]['capacity'] -= path_cp
                if RG.edge[u][v]['capacity'] == 0:
                    RG.remove_edge(u,v)

                if RG.has_edge(v,u):
                    RG.edge[v][u]['capacity'] += path_cp
                else:
                    RG.add_edge(v,u,capacity=path_cp)
            else:
                # then this edge is a "cancelling" flow
                # residue should go up and cancelling "capacity" should go down
                G.edge[v][u]['flow'] -= path_cp
                RG.edge[v][u]['capacity'] += path_cp
                RG.edge[u][v]['capacity'] -= path_cp
                if RG.edge[u][v]['capacity'] == 0:
                    RG.remove_edge(u,v)


if __name__ == '__main__':
    G = nx.gnm_random_graph(100,500,directed=True)

    while not nx.is_directed_acyclic_graph(G):
        G = nx.gnm_random_graph(100,500,directed=True)

    GG = G.copy()
    for u,v in G.edges_iter():
        GG[u][v]['weight'] = 1
    paths = nx.single_source_dijkstra_path(GG,0).values()

    s = 0
    t = max([(i,len(v)) for i,v in enumerate(paths)],key=itemgetter(1))[0]

    path = isthereapath(G,s,t)

    for u,v in G.edges_iter():
        G.edge[u][v]['capacity'] = random.random()

    edmondskarp(G,s,t)

    pos = nx.spring_layout(G)

# 26.2-11 turn the undirected graph into a directed graph by adding edges in each direction of weight 1.
# fix a vertex u. for each vertex v compute maxflow. by maxflow-mincut this equals the number of edges crossing the
# cut. taking the minimum over all of these cuts you get the minimum number of edges needed to disconnect
# u from some v for all u and v (because the graph is symmetric every run computer s=u t=v and s=v t=u).