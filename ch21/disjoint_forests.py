import random


class DisjointNode():
    # children is set of DisjointNodes
    def __init__(self,val=None,prnt=None,children:'set of nodes'=None):
        self.val = val
        self.prnt = prnt
        if children is None:
            self.children = set()
        else:
            for child in children:
                child.prnt = self
        self.next = None
        self.set = None

    def __str__(self):
        return str(self.val)

    def __iter__(self):
        return iter(self.children)

    def __next__(self):
        return next(iter(self))

    def print(self):
        return self.pprint([],True,[])

    # basically an inorder traversal
    # really clever
    def pprint(self,pref,isTail,sb):
        t = pref + list("└── " if isTail else "├── ") + list(str(self.val))
        sb.append(t)
        for child in list(self.children)[:-1]:
            child.pprint(pref + list("    " if isTail else "│   "), False, sb)
        if len(self.children) > 0:
            list(self.children)[-1].pprint(pref + list("    " if isTail else "│   "), True, sb)
        return sb

    def findset(self):
        stk = []
        ptr = self
        while ptr.prnt != ptr:
            stk.append(ptr)
            ptr = ptr.prnt

        while len(stk) > 0:
            stk.pop().prnt = ptr


class DisjointTree():
    def __init__(self,val):
        self.root = DisjointNode(val=val)
        self.root.prnt = self.root
        self.root.set = self
        self.rank = 0

    def __add__(self, other):
        if self.rank > other.rank:
            other.root.next = self.next
            self.next = other.root

            other.root.prnt = self.root
            self.root.children = self.root.children.union({other.root})
            # for child in other.children:
            #     child.prnt = self.root
            # self.children = self.children.union(other.children)
        elif self.rank < other.rank:
            self.root.next = other.next
            other.next = self.root
            self.root.prnt = other.root
            other.root.children = other.root.children.union({self.root})
            self.root = other.root
        else:
            rs = random.sample([self.root,other.root],2)

            rs[1].next = rs[0].next
            rs[0].next = rs[1]

            self.root = rs[0]
            rs[1].prnt = self.root
            self.root.children = self.root.children.union({rs[1]})
            self.root.rank += 1

        return self


# you need a dict of numbers associated with each node in the disjoint forest
# and a dict of disjoint trees keyed on representative.
# to do the join look up the node corresponding to the number, then do find set
# then look up the disjoint set for in the dict of disjoint sets
def offline_min(m,dict_disjoint_sets, dict_nodes,n):
    extracted = m*[None]
    for i in range(1,n+1):
        rep = dict_nodes[i].findset()
        j = dict_disjoint_sets.keys().index(rep)
        kj = dict_disjoint_sets.items()[j]
        if j != m+1:
            extracted[j+i] = i
            l = dict_disjoint_sets.keys()[j+1]
            kl = dict_disjoint_sets.items()[l]
            kj+kl
            del dict_disjoint_sets[rep]
    return extracted





# 21.1-3 worst case both linear (the rub is that find set is linear time too without path compression)
# and union is bad too

# 21.3-4 connect all the nodes up like a linked list? representative node points to first child. then when joining the other
# set is "spliced in": call the pointer next. when splicing in the next disjoint set take next of the joined-to set point it at the
# next of the representative of the joined in set, then put the next of the joined-in set to point to the original next or the joined-to
# set

# 21-2c let the pseudo distance be the distance from each node to its parent. when a findset happens the first time the updated
# pseudodistance is the sum of the pseudo distances to the root. its the findset path compression function that actually
# changes the shape of the tree, i.e. you could turn a tree into

# 21-2d join 