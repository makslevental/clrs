import numpy as np
from collections import deque
from functools import partial

def universal_sink(mat):

    shp = np.shape(mat)
    i = 0
    j = 1
    while i < shp[0] and j < shp[1]:
        if mat[i,j] == 0:
            j += 1
        elif mat[i,j] == 1:
            i += 1

    if i == 0:
        check = True
        for k in range(0,shp[0]):
            if mat[k,0] == 0:
                check = False
    elif i == shp[0]:
        check = True
        for k in range(0,i):
            if mat[k,j] == 0:
                check = False
    else:
        check = False

    return check


class Vertex():
    def __init__(self,name:str=None,value=None,children:dict=None):
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        if children is not None:
            self.children = children
        else:
            self.children = set()

        self.visited = 0
        self.distance = 0
        self.parent = None

    def __setattr__(self, item, value):
        setattr(self,item,value)
        return self

    def deg(self):
        return len(self.children)

class Graph():
    def __init__(self, vertices, edges):
        self.vertices = {}
        for v in vertices:
            self.vertices[v] = Vertex(name=str(v))
        # edges are directed. undirected graphs will be represented by double edges
        self.edges = edges
        for e in self.edges:
            self.vertices[e[1]].children.add(self.vertices[e[2]])

    def bfs(self,root=None):
        if root is not None:
            ptr = root
        else:
            ptr = self.vertices[1]

        ptr.distance = 0
        ptr.parent = None
        q = deque([ptr])
        while len(q) > 0:
            ptr = q.popleft()
            q.append(setattr(setattr(v,'parent',ptr),'distance',ptr.distance+1) for v in ptr.children if v.visited != 1)
            ptr.visited = 1

    def avg_degree(self):
        pass





# 22.1-1 outdegree is easy. constant time if you for example store the length of the adjacency list
# in degree is much harder |V|^2 for each vertex, so |V|^3. to solve the problem i would just construct
# the adjacency matrix representation first pass (easy: just traverse the adjacency list and mark entries in
# the matrix). then for each following query it would be just a sum across the Vth column

# 22.1-3 for the adjacency matrix representation the construction is constant time essentially (just traverse the matrix
# by its transpose. for adjacency list representation you could create a hash table of vertices then traverse all of the
# adjacency lists and hash on entries (vertices) then push to linked lists of those vertices the owener of that linked list

# 22.1-4 hash on (u,v). if there's a collision then don't insert in the new adjacency list

# 22.1-5 G^2 for adjacency matrix is just the normed square of the matrix because taking the dot product "turns on" connections
# to the 2 hop nodes. for adjacency-list i guess you have to just traverse each list. if you treat each adjacency list as a set
# you can do set union but those are still linear (n^2 == O(|V||E|))


# 22.1-6 start at top left. go right until you hit a 1. if you never hit one then there's no universal sink since that node
# is disconnected from all. when you hit a one continue down until you hit a zero or the bottom floor. if you never hit a zero then the
# vertex corresponding to that column where you hit is the only universal sink candidate (why only? because if there were another vertex
# with all 1s in its columns it would have two ones in its row). all that remains is to check that entire column for 1s. if you hit the right
# wall then there's no universal sink. there are two edge cases: if you hit the right wall on the first row the first vertex might be a
# universal sink. then you also need to check that the row of the universl sink vertex has only one 1 (otherwise there might be two "universal
# sinks")

# 22.1-7 only non-zero entries are on the diagonal and they're the total degree (in degree - out degree). wrong. off diagonal entries exist
# because nodes connected to each other have opposite sign entries in B_{}j. so off diagonal entries is -number of edges connecting vertex
# i to j.

# 22.2-3 look at my implementation: only push nodes that haven't been visited

# 22.2-7 2 color the graph: set the nodes in each round of the bfs to be the opposite color of the parent. if node is already colored same
# color then no such coloring is possible

# 22.2-8 start at any node and do a bfs. pick the node that's the farthest. then do another from that node picking the node that's the farthest

# 22.2-9 use the same walk as in tarjan's algorithm:
# walk(q)
# print(q)
# for v in q.children:
#   walk(v)
#   print(q)