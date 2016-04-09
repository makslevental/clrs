class Vertex():
    def __init__(self,name:str=None,value=None,children:dict=None):
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        else:
            self.parents = {}
        if children is not None:
            self.children = children
        else:
            self.children = {}



class Graph():
    def __init__(self,root=None):
        if root is not None:
            self.root = Vertex(name='root',value=root)



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
# is disconnected from all. when you hit a one go down until you hit a zero. if you never hit a zero