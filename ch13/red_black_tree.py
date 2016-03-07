from ch10.treenode import TreeNode
from ch12.bst import BinarySearchTree
from enum import Enum

class Color(Enum):
    RED = 1
    BLACK = 2


class RBTreeNode(TreeNode):
    def __init__(self, val=None, prnt=None, color=None, lchild=None, rchild=None):
        super().__init__(val, prnt, lchild, rchild)
        self.color = color

class RedBlackTree(BinarySearchTree):
    nodetype = RBTreeNode

    def __init__(self,ls=None):
        self.root = self.nodetype()
        if ls:
            self.ls = ls
            self.root.val = ls[0]
            self.root.color = Color.BLACK
            for v in ls[1:]:
                self.insert(v)

    def insert(self,x):
        ptr = super().insert(x)
        ptr.color = Color.RED

        # case 1 ptr's "uncle" is red (then both ptr's parent and uncle are red)
        # color both ptr.prnt black and ptr's "uncle" black and ptr's parent red (maintaining
        # rb property that same number of black nodes on all paths from root)
        # but then ptr's parent might violate so move up two levels
        def case1():
            nonlocal ptr, uncle
            c1 = (uncle.color == Color.RED)
            if c1:
                ptr.prnt.color = Color.BLACK
                uncle.color = Color.BLACK
                ptr.prnt.prnt = Color.RED
                ptr = ptr.prnt.prnt
            return c1

        # root is never red so
        # ptr and ptr.prnt might be red -> violation of property of rb tree
        while ptr.prnt.color == Color.RED:
            if ptr.prnt == ptr.prnt.prnt.lchild:
                uncle = ptr.prnt.prnt.rchild

                # case 2 and 3 ptr's "uncle" is black (and ptr's parent is black)
                # color ptr's uncle red and rotate right
                if not case1():
                    if ptr == ptr.prnt.rchild:
                        # rotate happens around the "top" node
                        ptr = ptr.prnt
                        self._left_rotate(ptr)
                        # now ptr is bottom left (after the rotation) and ptr.prnt is original inserted value
                        # color ptr.prnt (original inserted value) black and ptr.prnt.prnt red and then rotate
                        # around ptr.prnt.prnt to the right
                    ptr.prnt.color = Color.BLACK
                    ptr.prnt.prnt.color = Color.RED
                    self._right_rotate(ptr.prnt.prnt)
            else:#if ptr.prnt == ptr.prnt.prnt.rchild:
                uncle = ptr.prnt.prnt.lchild
                c1 = case1()
                if not c1:
                    if ptr == ptr.prnt.lchild:
                        ptr = ptr.prnt
                        self._right_rotate(ptr)
                    ptr.prnt.color = Color.BLACK
                    ptr.prnt.prnt.color = Color.RED
                    self._left_rotate(ptr.prnt.prnt)






    def _right_rotate(self,y):
        pry = y.prnt
        x = y.lchild
        # replace y with x
        if y == pry.lchild:
            pry.lchild = x
        else:
            pry.rchild = x
        x.prnt = pry

        # make y's left child x's right child
        y.lchild = x.rchild
        y.lchild.prnt = y
        # make y x's right child
        x.rchild = y
        y.prnt = x



    def _left_rotate(self,y):
        pry = y.prnt
        x = y.rchild
        # replace y with x
        if y == pry.lchild:
            pry.lchild = x
        else:
            pry.rchild = x
        x.prnt = pry

        # make y's right child x's left child
        y.rchild = x.lchild
        y.rchild.prnt = y
        # make y x's left child
        x.lchild = y
        y.prnt = x


