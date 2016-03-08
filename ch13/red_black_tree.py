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


    def delete(self,x):
        self.deleteroot(self[x])

    def deleteroot(self,nd):
        orig_color = nd.color
        # ptr is node that was moved to nd position
        # x is ptr child
        x,ptr = self.deleteroot(nd)
        ptr.color = nd.color

        if orig_color == Color.BLACK: # then x is "extra black"
            while x !=  self.root and x.color == Color.BLACK:
                if x == x.prnt.lchild:
                    sib = x.prnt.rchild
                    if sib.color == Color.RED: # case C, case 1 CLRS transformed to either case 2 or 3 (black sib)
                        sib.color = Color.BLACK
                        x.prnt.color = Color.RED
                        self._left_rotate(x.prnt)
                        sib = x.prnt.rchild

                    if sib.lchild.color == Color.BLACK and sib.rchild.color == Color.BLACK: # propagate extra blackness up
                        sib.color = Color.RED
                        x = x.prnt
                    else: # one of the sib's children is black and the other is red -> case 4
                        if sib.rchild.color == Color.BLACK:
                            sib.lchild.color = Color.BLACK
                            sib.color = Color.RED
                            self._right_rotate(sib)
                            sib = x.prnt.rchild
                        # case 4 sib's right child is red
                        sib.color = sib.prnt.color
                        sib.prnt.color = Color.BLACK
                        sib.rchild.color = Color.BLACK
                        self._left_rotate(sib.prnt)
                        x = self.root
                else:
                    sib = x.prnt.lchild
                    if sib.color == Color.RED: # case C, case 1 CLRS transformed to either case 2 or 3 (black sib)
                        sib.color = Color.BLACK
                        x.prnt.color = Color.RED
                        self._right_rotate(x.prnt)
                        sib = x.prnt.lchild

                    if sib.rchild.color == Color.BLACK and sib.lchild.color == Color.BLACK: # propagate extra blackness up
                        sib.color = Color.RED
                        x = x.prnt
                    else: # one of the sib's children is black and the other is red -> case 4
                        if sib.lchild.color == Color.BLACK:
                            sib.rchild.color = Color.BLACK
                            sib.color = Color.RED
                            self._left_rotate(sib)
                            sib = x.prnt.lchild
                        # case 4 sib's right child is red
                        sib.color = sib.prnt.color
                        sib.prnt.color = Color.BLACK
                        sib.lchild.color = Color.BLACK
                        self._right_rotate(sib.prnt)
                        x = self.root
            x.color = Color.BLACK

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


