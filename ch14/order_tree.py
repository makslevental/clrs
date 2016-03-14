import random

from ch13.red_black_tree import RedBlackTree, RBTreeNode, RBSENTINEL, Color

class ORDSENTINEL(RBSENTINEL):
    def __init__(self, prnt):
        super().__init__(prnt)
        self.size = 0

class OrderNode(RBTreeNode):
    SENTINEL = ORDSENTINEL

    # **kwargs mean capture in dict
    def __init__(self,*pargs):
        # **kwargs means unpack them as key value args
        super().__init__(*pargs)
        self.size = self.lchild.size + self.rchild.size + 1

    def __str__(self):
        return super().__str__() + ' sz:' + str(self.size)


class OrderTree(RedBlackTree):

    nodetype = OrderNode

    def __init__(self, ls=None):
        super()._init__()
        if ls:
            for v in ls:
                self.insert(v)

    def insert(self,x):
        new = super().insert(x)
        while new:
            new.size = new.lchild.size + new.rchild.size + 1
            new = new.prnt

    def select(self,i):
        # the root has rank r duh
        ptr = self.root
        r = ptr.lchild.size + 1
        while i != r:
            r = ptr.lchild.size + 1
            if i == r:
                return self.root.val
            elif i < r:
                ptr = ptr.lchild
            else:
                ptr = ptr.rchild
                # since the subtree root at ptr contains
                # r elements that precede ptr's right subtree in an inorder traversal
                # the ith smallest element in the tree rooted at ptr is (i-r)th element
                # in the tree rooted at ptr.rchild. basically each tree only know how many to
                # its left and so while including ptr there are r elements that precede
                # any element in the tree rooted at ptr.rchild
                i -= r
        return ptr.val

    def rank(self,x):
        # how many nodes is an arbitrary node to the right of?
        # well there's all the stuff to the left of it
        # and there's all the stuff the trees it's a part of are to the left of
        r = x.lchild.size + 1
        ptr = x
        while ptr != self.root:
            if ptr == ptr.prnt.rchild:
                r += ptr.prnt.lchild.size + 1
            ptr = ptr.prnt
        return r

    def keyrank(self,k):
        x = self.bsttraverse(k)
        return self.rank(x)

    def _left_rotate(self,y):
        yy,r = super()._left_rotate(y)
        r.size = yy.size
        yy.size = yy.lchild.size + yy.rchild.size + 1

    def _right_rotate(self,y):
        yy,l = super()._right_rotate(y)
        l.size = yy.size
        yy.size = yy.lchild.size + yy.rchild.size + 1

if __name__ == '__main__':
    ls = random.sample(range(100),15)
    o = OrderTree(ls)
    o.print()

# 14.1-5 duh find the order of x and then find the element whose order is r+i

# 14.1-7 how far an element is ahead of its rank is how many inversions there are
# that include that element. if an element is behind its rank (closer to first)
# then it will appear as inversion for other elements. so find an element's rank
# and how much its position differs from its rank. if it differes by a negative amount
# then don't count it. otherwise it's j - r(j), where r(j) is its rank.

# 14.1-8 go around the circle counter clockwise. every time you reach an endpoint "label" it and
# push it to an array. also label it's polar opposite something else (in order to distinguish
# the line as already being encountered). When you run out of unlabeled points go around in the
# same point as where you start but now push only the endpoints that have been labeled opposites
# now treat one array as the correct order and the other one as having inversions. use
# above trick with order statistic tree