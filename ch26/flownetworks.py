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


    if len(path) > 0:
        return list(reversed(list(zip(path+[s],[t]+path))))
    else:
        return path


def edmondskarp(G: nx.Graph, s, t):

    RG = G.copy()

    for u,v in G.edges_iter():
        G.edge[u][v]['flow'] = 0

    path = isthereapath(RG,s,t)
    while len(path) > 0:
        path_cp = min([RG.edge[u][v]['capacity'] for u,v in path])
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
        path = isthereapath(RG,s,t)

    return RG

def mincut(G,RG,s,t):
    dtree = nx.dfs_tree(RG,s)
    cut = []
    for u in dtree.nodes_iter():
        for v in G.edge[u].keys():
            if v not in dtree.node:
                cut.append((u,v))
    return cut


if __name__ == '__main__':
    G = nx.DiGraph([(0,1,{'capacity':16}),(0,2,{'capacity':13}),
                    (1,3,{'capacity':12}),
                    (2,1,{'capacity':4}),(2,4,{'capacity':14}),
                    (3,2,{'capacity':9}),(3,5,{'capacity':20}),
                    (4,3,{'capacity':7}),(4,5,{'capacity':4}),
                    ])
    s = 0
    t = 5
    RG = edmondskarp(G,s,t)
    mincut(G,RG,s,t)

    pos = nx.spring_layout(G)

# 26.2-11 turn the undirected graph into a directed graph by adding edges in each direction of weight 1.
# fix a vertex u. for each vertex v compute maxflow. by maxflow-mincut this equals the number of edges crossing the
# cut. taking the minimum over all of these cuts you get the minimum number of edges needed to disconnect
# u from some v for all u and v (because the graph is symmetric every run computer s=u t=v and s=v t=u).

# 26-1a vertex a = 2 vertices a' and a''. a' only has incoming edges on a, a'' only has outgoing on a, then finally
# there's one edge (a',a'') with capacity equal to the vertex capacity.
# 26-1b create a virtual source from every escape coordinate pair, create a virtual sink from all border vertices
# enforce vertex capacity 1. done.

# 26-2 this works because it picks up as many edges as possible (maximum bipartite matching)

# 26-4a just run 1 iteration of ford-fulkerson
# 26-4b define f'(x,y) = f(x,y) except on the edge with reduced capacity, where f'(u,v) = f(u,v)-1. f' obeys
# capacity constraints but is not a legal flow because there is 1 more flow unit entering u than leaving, and 1 more
# leaving v than entering (since we just arbitrarily reduced the flow on (u,v) of already calculated f(u,v). the
# solution is to reroute the extra unit of flow between u and v. search for an augmenting path from u to v:
# if one exists then augment the flow. if one does not exist then reduce the flow from s to u by augmenting the flow
# from s to u (i.e. find an augmenting path from u to s, which exists because there is flow from s to u). similarly reduce
# the flow from v to t by augmenting the flow from t to v.

# 26-6a the M+1 thing is obvious because there are at least 2j+1 edges in an augmenting paths where j edges are already
# in the matching. so the extra edge matches another pair of vertices. then since the paths required to be
# vertex disjoint M + (P1 u P2 u P3 ... u Pk) = |(((M+P1)+P2)...)+Pk| = |M|+k
# 26-6g something bfs two coloring?