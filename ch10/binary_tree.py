import random
from collections import deque



class TreeNode:
    def __init__(self,val,prnt=None,lchild=None,rchild=None):
        self.val = val
        self.prnt = prnt
        self.lchild = lchild
        self.rchild = rchild

    def __str__(self):
        return str(self.val)
        # return ','.join([str(self.prnt.val) if self.prnt else '#',
        #                str(self.val),
        #                str(self.lchild.val) if self.lchild else '#',
        #                str(self.rchild.val) if self.rchild else '#'])

    def __iter__(self):
        return iter([self.lchild,self.rchild])

    def __next__(self):
        try:
            ch = next(self.childit)
        except StopIteration:
            self.childit = iter(self.children)
            ch = next(self.childit)

        return ch

SENTINEL = lambda x: TreeNode('#',prnt=x)

class BinaryTree:
    def __init__(self,ls=None):
        if ls:
            self.root = TreeNode(ls[0])
            self.root.lchild = SENTINEL(self.root)
            self.root.rchild = SENTINEL(self.root)
            self.end = deque([iter(self.root)])

        for v in ls[1:]:
            self.insert(v)

    def insert(self,x):
        nxtnode = self.end[0]
        try:
            leaf = next(nxtnode)
        except StopIteration:
            self.end.popleft()
            nxtnode = self.end[0]
            leaf = next(nxtnode)

        leaf.val = x
        leaf.lchild = SENTINEL(leaf)
        leaf.rchild = SENTINEL(leaf)
        self.end.append(iter(leaf))

    def __str__(self):
        q = deque()
        q.append(self.root)
        rep = []
        while len(q) > 0:
            node = q.popleft()
            rep.append(node.val)
            if node.lchild and node.lchild.val != '#':
                q.append(node.lchild)
                if node.rchild and node.rchild.val != '#':
                    q.append(node.rchild)

        return ','.join(str(x) for x in rep)
if __name__ == '__main__':

    b = BinaryTree(random.sample(range(100), 10))
    print(b)


# 10.4-2 depth first search
# 10.4-3 duh