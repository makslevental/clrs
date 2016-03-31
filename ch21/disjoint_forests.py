from ch10.treenode import TreeNode
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

class DisjointTree():
    def __init__(self,val):
        self.root = DisjointNode(val=val)
        self.root.prnt = self.root
        self.rank = 0

    def __add__(self, other):
        if self.rank > other.rank:
            other.root.prnt = self
            self.root.children = self.root.children.union({other.root})
            # for child in other.children:
            #     child.prnt = self.root
            # self.children = self.children.union(other.children)
        elif self.rank < other.rank:
            self.root.prnt = other.root
            other.root.children = other.root.children.union({self.root})
            self.root = other.root
        else:
            rs = random.sample([self.root,other.root],2)
            self.root = rs[0]
            self.root.children = self.root.children.union({rs[1]})
            self.root.rank += 1

