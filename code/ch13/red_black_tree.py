from ch10.treenode import TreeNode
from ch12.bst import BinarySearchTree, TreeObserver
from enum import Enum
import random
import tkinter
import tkinter.font as font

class Color(Enum):
    RED = 1
    BLACK = 2


class RBSENTINEL:
    color = Color.BLACK

    def is_sent(self):
        return True

    def __init__(self,prnt):
        self.prnt = prnt

    def __bool__(self):
        return False

    def __str__(self):
        return 'SENT'



class RBTreeNode(TreeNode):

    SENTINEL = RBSENTINEL

    def __init__(self, val=None, prnt=None, color=None, lchild=None, rchild=None):
        super().__init__(val, prnt, lchild, rchild)
        if not lchild:
            self.lchild = self.SENTINEL(self)
        if not rchild:
            self.rchild = self.SENTINEL(self)
        if not prnt:
            self.prnt = self.SENTINEL(None)
        self.color = color

    def __str__(self):
        if self.color:
            c = 'B' if self.color == Color.BLACK else 'R'
        else:
            c = ''
        return super().__str__()+' '+c

class RedBlackTree(BinarySearchTree):
    nodetype = RBTreeNode


    def __init__(self,ls=None):
        super()._init__()
        if ls:
            for v in ls:
                self.insert(v)

    def insert(self,x):
        orig_new = new = super().insert(x)
        new.color = Color.RED
        self._announce()

        # case 1 new's "uncle" is red (then both new's parent and uncle are red)
        # color both new.prnt black and new's "uncle" black and new's parent red (maintaining
        # rb property that same number of black nodes on all paths from root)
        # but then new's parent might violate so move up two levels
        def case1():
            nonlocal new, uncle
            c1 = (uncle.color == Color.RED)
            if c1:
                new.prnt.color = Color.BLACK
                uncle.color = Color.BLACK
                new.prnt.prnt.color = Color.RED
                self._announce()
                new = new.prnt.prnt
            return c1

        # new and new.prnt might be red -> violation of property of rb tree
        while new.prnt.color == Color.RED:
            if new.prnt == new.prnt.prnt.lchild:
                uncle = new.prnt.prnt.rchild

                # case 2 and 3 new's "uncle" is black (and new's parent is red)
                # color new's uncle red and rotate right
                if not case1():
                    if new == new.prnt.rchild:
                        # rotate happens around the "top" node
                        new = new.prnt
                        self._left_rotate(new)

                    # now new is bottom left (after the rotation) and new.prnt is original inserted value
                    # color new.prnt (original inserted value) black and new.prnt.prnt red and then rotate
                    # around new.prnt.prnt to the right
                    new.prnt.color = Color.BLACK
                    new.prnt.prnt.color = Color.RED

                    self._right_rotate(new.prnt.prnt)

            else:  # if new.prnt == new.prnt.prnt.rchild:
                uncle = new.prnt.prnt.lchild
                if not case1():
                    if new == new.prnt.lchild:
                        new = new.prnt
                        self._right_rotate(new)

                    new.prnt.color = Color.BLACK
                    new.prnt.prnt.color = Color.RED
                    self._announce()
                    self._left_rotate(new.prnt.prnt)

        self.root.color = Color.BLACK
        self._announce()
        return orig_new

    def delete(self,x):
        self.deleteroot(self[x])

    def deleteroot(self,nd):
        orig_color = nd.color
        # ptr is node that was moved to nd position
        # x is ptr child
        x,ptr,orig_color = super().deleteroot(nd)
        ptr.color = nd.color
        self._announce()
        if orig_color == Color.BLACK: # then x is "extra black"
            while x != self.root and x.color == Color.BLACK:
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
        l = y.lchild
        y.lchild = l.rchild
        if not l.rchild is None:
            l.rchild.prnt = y
        l.prnt = y.prnt
        if not y.prnt:
            self.root = l
        elif y == y.prnt.rchild:
            y.prnt.rchild = l
        else:
            y.prnt.lchild = l
        l.rchild = y
        y.prnt = l

        self._announce()
        return y,l

    def _left_rotate(self,y):
        r = y.rchild
        y.rchild = r.lchild
        if not r.lchild is None:
            r.lchild.prnt = y
        r.prnt = y.prnt
        if not y.prnt:
            self.root = r
        elif y == y.prnt.rchild:
            y.prnt.rchild = r
        else:
            y.prnt.lchild = r
        r.lchild = y
        y.prnt = r

        self._announce()
        return y,r


class simpleapp_tk(tkinter.Tk):


    def __init__(self,parent,ls,b):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.ls = ls
        self.b = b
        self.it = iter(ls)
        self.initialize()


    def initialize(self):
        self.grid()

        self.entry = tkinter.Entry(self)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Key>", self.OnWrite)

        self.labelVariable = tkinter.StringVar()
        self.labelVariable.set("")
        appHighlightFont = font.Font(family='Courier', size=12)
        label = tkinter.Label(self,
                              anchor="w",fg="white",bg="blue", height=0, justify="left", textvariable=self.labelVariable,font=appHighlightFont)
        label.grid(column=0,row=1,columnspan=5,sticky='EW')

        self.grid_columnconfigure(0,weight=1)

    def OnWrite(self, event):
        letter = event.char.encode('utf-8')
        # suggestions = ",".join(map(lambda x: word+x[1:],[w for w,_ in self.r[0:10]]))
        # self.b.insert(next(self.it))

        self.update()
        str = self.b.print()
        # print(str)
        self.labelVariable.set(str)





if __name__ == '__main__':
    ls = random.sample(range(100),15)
    # ls = [11, 53, 35, 29, 19, 8, 6, 99, 66, 28, 45, 82, 85, 51, 2]
    b = RedBlackTree()
    t = TreeObserver(b)
    b.insert(5)
    # b.print()
    # #

    # b.inorderstack()

    # r = random.sample(range(100),1)[0]
    # r = 63
    # print(sorted(ls))
    # print(r,b.succ(r))
    # print()
    # print(r,b.predec(r))
    b.print()
    #
    # app = simpleapp_tk(None,ls,b)
    # app.title('Spelling Suggestion')
    # app.mainloop()
    # while True:
    #     d = int(input("delete: "))
    #     b.delete(d)
    #     b.print()