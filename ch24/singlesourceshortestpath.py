import matplotlib.pyplot as plt
import networkx as nx
import random
from heapdict import heapdict

def initialize(G,s):
    for n in G:
        G.node[n] = {'distance': float("inf"), 'parent': None, 'children': set()}
    G.node[s]['distance'] = 0

def relax(G,u,v):
    if G.node[v]['distance'] > G.node[u]['distance'] + G.edge[u][v]['weight']:
        G.node[v]['distance'] = G.node[u]['distance'] + G.edge[u][v]['weight']
        G.node[v]['parent'] = u

def bellmanford(G,s):
    initialize(G,s)
    for _ in range(len(G.node)-1):
        for u, v in G.edges_iter():
            relax(G, u, v)

    for u, v in G.edges_iter():
        # the longest "shortest path" is |V|-1 edges. if any other edges
        # can be updated that means the shortest path is |V| edges, which means there's
        # a negative weight cycle
        if G.node[v]['distance'] > G.node[u]['distance'] + G.edge[u][v]['weight']:
            return False

    for v in G.nodes_iter():
        prnt = G.node[v]['parent']
        if prnt:
            G.node[prnt]['children'].add(v)

    return True


def dijkstra(G, s):
    initialize(G,s)
    q = heapdict()
    for v,d in G.nodes_iter(data=True):
        q[v] = d['distance']

    done = set()
    while len(q) > 0:
        u,d = q.popitem()
        done.add(u)
        for v in G.edge[u]:
            if v not in done:
                relax(G,u,v)
                q[v] = G.node[v]['distance']

    for v in G.nodes_iter():
        prnt = G.node[v]['parent']
        # prime example where is not None is important
        if prnt is not None:
            G.node[prnt]['children'].add(v)

def number_paths_dag(G):
    for v in G.nodes_iter():
        G.node[v]['paths'] = 0
    t_sort = nx.topological_sort(G)
    for u in t_sort:
        for v in G.edge[u]:
            G.node[v]['paths'] += G.node[u]['paths'] + 1

    paths = 0
    for v,d in G.nodes_iter(data=True):
        paths += d['paths']

    return paths


def pprint(G, root, pref, istail, sb):
        t = pref + list("└── " if istail else "├── ") + list(str(root))
        sb.append(t)
        children = list(G.node[root]['children'])
        for child in children[:-1]:
            pprint(G,child, pref + list("    " if istail else "│   "), False, sb)
        if len(children) > 0:
            pprint(G,children[-1], pref + list("    " if istail else "│   "), True, sb)
        return sb

def treeprint(G,root):
    print(*map(lambda x: ''.join(x), pprint(G,root, [], True, [])), sep='\n')


if __name__ == '__main__':
    # i don't know what directed True/False is supposed to do but
    # it doesn't add more edges so?
    G = nx.fast_gnp_random_graph(10,.3,directed=True)
    while not nx.is_directed_acyclic_graph(G):
        G = nx.fast_gnp_random_graph(10,.3,directed=True)

    pos = nx.spring_layout(G)

    # plt.ion()
    # fig = plt.figure(221)

    for u,v in G.edges_iter():
        G.edge[u][v]['weight'] = random.random()


    print(number_paths_dag(G))

    # dijkstra(G,0)
    # treeprint(G,0)


    # print(bellmanford(G,1))
    # treeprint(G,1)



    edge_labels=dict([((u,v,),round(d['weight'],3))
                 for u,v,d in G.edges(data=True)])
    nx.draw_networkx_nodes(G,pos)
    nx.draw_networkx_labels(G,pos,labels={n:n for n in range(len(G.node))})
    nx.draw_networkx_edges(G,pos,arrows=True)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,label_pos=0.5)

    plt.show()

# 24.1-3 keep tabs on whether any relaxations happened. if none then stop

# 24.1-5 create a universal source, and compute bellmanford from the universal source. shortest negative paths
# will be those chosen by this bellmanford run. if there are no vertices which are "negatively" close then
# just compute G^T and find outgoing edge with smallest weight

# 24.1-6 run bellmanford. if the second for loop returns false record which vertex (u,v). to find the shortest cycle
# run bellman ford with new source v to find path to u. to find some cycle just trace pointer chains

# 24.2-4 basically the dp algorithm in 22.4. set the "distance" function for each node to 1 and then do a top sort and then
# in topsort order compute "distance" to be the sum of "distances" of edge going into the node.

# 24.3-4 key is to check whether any deltas can be further relaxed. the rest are consistency check: check tree is actually tree
# check distance from s to s is 0, check distance to vertex is equal to distance to parent plus edge weight.

# 24.3-6 there are two ways to do this. first define f(u,v) as the probability of failure. then we want to minimize prod(f(u,v)) over paths
# taking log we get min sum(log(f(u,v)) which is shortest path. some details about negativity but otherwise use dijkstra's. alternatively
# you can modify dijkstra to look for max-ish paths by extract-max and relaxing if v.d < u.d*r(u,v). although i don't exactly
# understand why works since isn't necessarily a dag (nor would this be the algo). if the graph was a dag then to find the longest path
# do top sort/shortests path on -G. this picks out the most negative edges, ie the longest path in G.

# shortest cycle including s positive graph dijkstra: do dijkstra and then use distances computed to find shortest cycle (look through edges
# of all vertices to see if they connect back to s).

# 24.3-7 duh this is exactly the idea you have when you meet bfs: if the edges were integers then just adding "virtual nodes"
# enable you to solve shortest path using bfs

# 24.3-8 use radix sort or something. i.e. "bucketize" vertices according to their distance from s. since max weight wedge is W there are a max
# of (V-1)W buckets. examine the buckets one by one in increasing order of distances in bucket (moving vertices from bucket to bucket.

# 24.4-3 can't be greater or equal to zero.

# 24.4-4 easy duh sum of weights over all paths.

# 24.4-5 what's the modification exactly? doesn't the shim come from transforming the constraint matrix
# into the incidence matrix? and adding the universal source?

# 24.4-6 rewrite the equality constraints as two inequality constraints

# 24.4-7 probably the same as how you run dfs on all nodes on an unconnected graph: by running the main loop
# in a for loop over all of the vertices
