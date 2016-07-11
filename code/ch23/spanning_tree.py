import copy
import random
from heapq import heappop, heappush, heapify
from operator import getitem, itemgetter
from ch6.heap import MinHeap
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import networkx.drawing.nx_pylab as nxx
# fuck everything i built.
# going to use adjacency matrix and just sets



pq = []                         # list of entries arranged in a heap
entry_finder = {}               # mapping of tasks to entries
REMOVED = '<removed-task>'      # placeholder for a removed task
counter = itertools.count()     # unique sequence count

def add_task(task, priority=0):
    'Add a new task or update the priority of an existing task'
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heappush(pq, entry)

def remove_task(task):
    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

def pop_task():
    'Remove and return the lowest priority task. Raise KeyError if empty.'
    while pq:
        priority, count, task = heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')


def kruskal_mst(num_v: int, edges: [tuple]):

    vertices = [{i} for i in range(num_v)]

    mst = []
    edges = list(sorted(edges,key=itemgetter(2)))
    for u,v,w in edges:
        if vertices[u] != vertices[v]:
            mst.append((u,v,w))
            v_union = vertices[u] | vertices[v]
            for x in v_union:
                vertices[x] = v_union

    return mst

# clearly broken because my implementation of heap
def prim_mst(num_v: int, edges: [tuple]):
    adj_mat = [[float("inf") for _ in range(num_v)] for _ in range(num_v)]
    for u,v,w in edges:
        adj_mat[u][v] = w

    global pq, entry_finder, REMOVED
    for i in range(num_v):
        add_task(i,float("inf"))
    heapify(pq)
    add_task(8,0)

    parents = {}
    try:
        while pq:
            u = pop_task()
            for v,w in enumerate(adj_mat[u]):
                if v in entry_finder and entry_finder[v] is not REMOVED and w < entry_finder[v][0]:
                    parents[v] = u,w
                    add_task(v,w)
    except KeyError:
        pass
    return sorted(parents.items(), key=itemgetter(0))


# 23.2-2
def prim_mst_simple(adj_mat):
    potentiates = [[float("inf"), (-1, -1)] for _ in range(len(adj_mat))]
    r = 0

    while True:
        for v, key in enumerate(adj_mat[r]):
            if v != r and key < potentiates[v][0]:
                potentiates[v] = [key, (v, r)]

        potentiates[r][0] *= -1
        try:
            minn = min(filter(lambda x: x[0] > 0, potentiates), key=itemgetter(0))
        except ValueError:
            return potentiates
        r = minn[1][0]





if __name__ == '__main__':
    num_v = 10
    # connectivity = 2/num_v
    # adj_mat = [[float("inf") for _ in range(num_v)] for _ in range(num_v)]
    # edges = []
    # for u,uu in enumerate(copy.deepcopy(adj_mat)):
    #     for v,_ in enumerate(uu):
    #         if random.random() <= connectivity:
    #             adj_mat[u][v] = random.random()
    #
    # for u in range(num_v):
    #     adj_mat[u][u] = float("inf")
    #     for v in range(u+1,num_v):
    #         adj_mat[u][v] = adj_mat[v][u]
    #         if adj_mat[u][v] < float("inf"):
    #             edges.append((u,v,adj_mat[u][v]))
    #             edges.append((v,u,adj_mat[u][v]))
    #




    # # edges = random.sample([(u,v,random.random()) for u in range(num_v) for v in range(num_v)],connectivity*num_v)
    #
    # # print(*edges)
    # print()
    # # edges = [(0, 8, 0.41579155951332647), (8, 0, 0.41579155951332647), (1, 6, 0.8695634223402718), (6, 1, 0.8695634223402718), (2, 3, 0.030658863658873714), (3, 2, 0.030658863658873714), (6, 7, 0.7017233991895718), (7, 6, 0.7017233991895718), (6, 8, 0.13379091009457134), (8, 6, 0.13379091009457134), (7, 8, 0.8888190765150605), (8, 7, 0.8888190765150605), (8, 9, 0.40790022037809937), (9, 8, 0.40790022037809937), (0, 9, 0.40952211879323763), (1, 7, 0.01565450539701374), (2, 7, 0.012632531745452091), (3, 2, 0.2837873936999862), (4, 3, 0.03702855274247174), (5, 1, 0.49283582494219935), (6, 8, 0.2051813595098967), (7, 1, 0.4719735178990171), (8, 7, 0.868093488025026), (9, 2, 0.8437543211721866)]
    # edges = [(0, 4, 0.8245585533577207) ,(4, 0, 0.8245585533577207) ,(0, 6, 0.2039168435635701) ,(6, 0, 0.2039168435635701) ,(0, 9, 0.9143560907478429) ,(9, 0, 0.9143560907478429), (1, 7, 0.26067611245184985) ,(7, 1, 0.26067611245184985), (1, 9, 0.684413116209369) ,(9, 1, 0.684413116209369) ,(2, 9, 0.7669884351038256) ,(9, 2, 0.7669884351038256) ,(3, 5, 0.6903211395777211), (5, 3, 0.6903211395777211), (3, 6, 0.5292942285586851), (6, 3, 0.5292942285586851), (5, 6, 0.889797676009428), (6, 5, 0.889797676009428) ,(6, 8, 0.9573958623797792) ,(8, 6, 0.9573958623797792), (6, 9, 0.5236856539750493), (9, 6, 0.5236856539750493) ,(7, 9, 0.20725051448877374) ,(9, 7, 0.20725051448877374)]
    # print(*edges,sep='\n')
    # print()
    # adj_mat = [[float("inf") for _ in range(num_v)] for _ in range(num_v)]
    # for u,v,w in edges:
    #     adj_mat[u][v] = w

    # edges.extend([(i,random.randint(0,num_v-1),random.random()) for i in range(num_v)]) # enforce connected (maybe?)

    # print(*adj_mat,sep='\n')

    # kmst = kruskal_mst(num_v,edges)
    # print(*sorted(kmst),sep='\n')
    # print(sum([w for _,_,w in kmst]))
    # print()
    # pmst = prim_mst(num_v,edges)
    # print(*sorted(pmst),sep='\n')
    # print(sum([c[1] for p,c in pmst]))
    # print()
    # pmst_simp = prim_mst_simple(adj_mat)
    # print(*sorted(pmst_simp),sep='\n')
    # print(sum([key for key,edge in pmst_simp if key != float("-inf")]))
    # print()

    G=nx.erdos_renyi_graph(10,0.45)
    # G = nx.Graph()
    # G.add_nodes_from(range(num_v))
    # G.add_edges_from([(u,v,{'weight':w}) for u,v,w in edges])
    # print(nx.is_connected(G))
    # # str_comps = nx.connected_components(G)
    # print(*nx.connected_components(G))
    # print(nx.number_connected_components(G))
    # nxmst = sorted(nx.minimum_spanning_tree(G).edges(data=True))
    # print(*nxmst,sep='\n')
    # print(sum([e[2]['weight'] for e in nxmst]))




    plt.figure(0)
    nx.draw_networkx(G)
    # nx.draw_networkx_edge_labels(G,pos=nx.drawing.draw_spring(G),edge_labels=nx.get_edge_attributes(G,'weight'))
    # plt.draw()
    # H = nx.Graph()
    # H.add_nodes_from(range(num_v))
    # H.add_edges_from([(u,v) for u,v,w in kmst])
    # print(nx.is_connected(H))
    # plt.figure(1)
    # nx.draw(H)
    # plt.draw()

# 23.1-1 assume that it doesn't. then for no minimum spanning tree is (u,v) in E. so take an arbitrary such tree.
# adding (u,v) creates a cycle from which we can remove any edge and preserve connectivity of the graph. therefore
# remove any edge other than (u,v). this produces a potentially different minimum spannign tree. contradiction.

# 23.1-2 umm you can use any edge to bridge S,V-S, not just light edges.

# 23.1-3 remove the edge and you disconnect the graph. so it's clearly a safe edge. if it weren't light then
# we would have picked the lighter edge to be in the minimum spanning tree and the original one wouldn't have been
# a minimum spanning tree

# 23.1-11 add the edge to create a cycle then dfs to find the edge on that cycle of highest weight

# 23.2-4 radix sort something something

# 23.2-5 radix sort something something

# 23.2-6 ?

# 23.2-7 throw in all the edges adjacent on the new vertex and run either kruskal's or prim's on the mst + new graph

# 23-1a something something unique weights
# 23-1b isn't this like literally the definition of second-best minimum spannign tree?
# 23-1c just do dfs on the spanning tree. since there are no cycles and only |V|-1 edges each run takes O(|V|) time.
# run it for all vertices (and even with repeats) you get O(|V|^2) running time.
# 23-1d by part b you only need to flip one edge to get from mst to second best mst. so compute mst on ElgV time.
# use part c to compute all max weight edges. then for all the edges in E but not in T find the one such that
# that edges weight minus max[u,v] is smallest. then adding that edge and removing the max[u,v] edge adds the smallest
# difference the minimum spanning tree.