from operator import itemgetter

import numpy as np
from collections import deque
import random
from itertools import product
import copy


# this is all so bad. it should be adjacency matrix and
# vertices should be indexes into a struct array or something (instead of storing anything)

# silly python designers
class Deque(deque):
    def pop(self):
        return self.popleft()


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


class GraphError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Vertex(object):
    def __init__(self, name: str, value=None, children: list=None, parent: 'Vertex'=None) -> None:
        if name is not None:
            self.name = name
        else:
            raise GraphError("Vertex must be named")

        self._value = value
        self.children = children if children is not None else []

        self.visited = False
        self.distance = 0
        self.parent = parent
        self.tree = set()

    def __str__(self):
        if self.value is not None:
            return repr(self.value)
        else:
            return self.name
    @property
    def value(self):
        if self._value is not None:
            return self._value
        else:
            return int(self.name)

    @value.setter
    def value(self, x):
        self._value = x


    def set(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    def deg(self):
        return len(self.children)





class Graph(object):
    def __init__(self, vertices: list, edges: [tuple]) -> None:
        self.vertices = len(vertices)*[None]
        for i, v in enumerate(vertices):
            self.vertices[i] = Vertex(name=str(v))
        # edges are directed. undirected graphs will be represented by double edges
        self.edges = edges
        self.adjmat = [[i-1]+(len(vertices))*[0] for i in range(len(vertices)+1)]
        self.adjmat[0] = [0]+list(range(0,len(vertices)))
        for e in self.edges:
            self.vertices[e[0]].children.append(self.vertices[e[1]])
            self.adjmat[e[0]+1][e[1]+1] = 1

    def bfs(self, root: Vertex=None):
        distance = lambda ptr: ptr.distance + 1

        for v in self.vertices:
            v.visited = False
            v.distance = 0
            v.parent = None

        return self.__fs(Deque, distance, root)

    def dfs_plain(self, root: Vertex=None):
        x = 0
        def timer(_):
            nonlocal x
            x += 1
            return x

        for v in self.vertices:
            v.visited = False
            v.distance = 0
            v.parent = None

        return self.__fs(list, timer, root)

    def __fs(self, typ, metric, root: Vertex=None):
        if root is not None:
            vertices = [root]
        else:
            vertices = self.vertices

        for v in vertices:
            ptr = v

            vert_order = []
            ptr.distance = metric(ptr)

            cont = typ()
            cont.append(ptr)

            while len(cont) > 0:
                ptr = cont.pop()
                if ptr.visited:
                    continue
                else:
                    vert_order.append(ptr)
                    ptr.visited = True
                    cont.extend([v.set(parent=ptr, distance=metric(ptr))
                                for v in ptr.children if v.visited is not True])

        for v in self.vertices:
            ptr = v
            while ptr.parent is not None:
                ptr.parent.tree.add(ptr)
                ptr = ptr.parent

        return vert_order

    def dfs_top(self,root: Vertex=None):
        for v in self.vertices:
            v.parent = None
            v.visited = False

        if root is not None:
            vertices = [root]
        else:
            vertices = self.vertices

        top_sorts = []

        for v in vertices:
            ptr = v
            # need to indicate opened and finished
            stk = [[ptr, False]]
            top_sort = []
            while len(stk) > 0:
                ptr, done = stk[-1]
                if done:
                    stk.pop()
                    top_sort.append((ptr, ')'))
                elif ptr.visited:
                    stk.pop()
                else:
                    ptr.visited = True
                    stk[-1][1] = True
                    top_sort.append((ptr,'('))
                    stk.extend([[v.set(parent=ptr), False] for v in ptr.children if v.visited is not True])

            if len(top_sort)>0:
                top_sorts.append(top_sort)

        for v in self.vertices:
            ptr = v
            while ptr.parent is not None:
                ptr.parent.tree.add(ptr)
                ptr = ptr.parent

        return top_sorts

    def strongly_conn_comp(self):
        # top sorts come out already reversed
        top_sorts = [[v for v,paren in tps if paren == ')'] for tps in self.dfs_top()]
        g_trans = [Vertex(name=str(v)) for v in range(len(self.vertices))]
        for v in self.vertices:
            for e in v.children:
                g_trans[int(e.name)].children.append(g_trans[int(v.name)])

        for v in g_trans:
            v.visited = False
            v.parent = None

        components = []
        for top_sort in top_sorts:
            for v in top_sort:
                component = self.__fs(list,lambda x: 0,g_trans[int(v.name)])
                components.append(component)

        for v in g_trans:
            ptr = v
            while ptr.parent is not None:
                ptr.parent.tree.add(ptr)
                ptr = ptr.parent

        return components

    def pprint(self, ptr: Vertex, pref: list, istail: bool, sb: list):
        t = pref + list("└── " if istail else "├── ") + list(str(ptr))
        sb.append(t)
        for child in list(ptr.tree)[:-1]:
            self.pprint(child, pref + list("    " if istail else "│   "), False, sb)
        if len(ptr.tree) > 0:
            self.pprint(list(ptr.tree)[-1], pref + list("    " if istail else "│   "), True, sb)
        return sb

    def treeprint(self,root):
        print(*map(lambda x: ''.join(x), self.pprint(root, [], True, [])), sep='\n')


if __name__ == '__main__':
    # num_v = int(input("num vertices"))
    # connectivity = int(input("connectivity"))
    num_v = 1000
    connectivity = 1
    print('\n')
    vertices = list(range(0, num_v))
    edges = random.sample(list(product(vertices, vertices)), connectivity*num_v)
    g = Graph(vertices, edges)
    print(*g.adjmat,sep='\n')
    print('\n')
    components = g.strongly_conn_comp()
    for component in components:
        if len(component) > 0:
            g.treeprint(component[0])
            print('\n')
    # tp_sorts = g.dfs_top()
    # for t in tp_sorts:
    #     print(''.join(list(map(lambda x: str(x[0]),t))),''.join(list(map(itemgetter(1),t))),sep='\n')
    #     g.treeprint(t[0][0])
    #     print('\n')



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

# 22.4-2 dynamic programming. the number of paths from s to t is the sum number of paths from t to each of s's parents, and on.
# do a topological sort first in order to figure out which nodes are potentially t's parents. the number of paths from s to s is 0.
# the number of paths from s to s+1 is 1 if there' an edge from s to s+1, etc.

# 22.4-4 do a dfs search but quit as soon as you hit a back edge. if there's a cycle then there will be > |V| edges and so the dfs will
# stop after |V| edges. if there's no cycle then the dfs will stop naturally after |V|-1 edges.