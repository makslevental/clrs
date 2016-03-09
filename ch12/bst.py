from ch10.treenode import TreeNode

import random

class TreeObserver:
    def __init__(self,tree):
        self.tree = tree
        self.tree.bind_to(self.update_view)

    def update_view(self):
        self.tree.print()

class BinarySearchTree:

    nodetype = TreeNode

    def _announce(self):
        for callback in self._observers:
            callback()

    def __init__(self,ls=None):
        self.root = self.nodetype()
        self._observers = []
        if ls:
            self.ls = ls
            self.root.val = ls[0]

            self._announce()

            for v in ls[1:]:
                self.insert(v)

    def bind_to(self,callback):
        self._observers.append(callback)

    # i want leaves to have nones as children
    def insert(self,x):
        if self.root.val is None:
            self.root.val = x
            return self.root
        # bsttraverse returns when ptr == none
        ptr = self.bsttraverse(x)

        if x <= ptr.val:
            ptr.lchild = self.nodetype(x,ptr)
            self._announce()

            return ptr.lchild
        else:
            ptr.rchild = self.nodetype(x,ptr)
            self._announce()
            return ptr.rchild

    #12.1-4 super annoying
    def inordernostack(self):
        prev = self.root
        crnt = self.root
        while True:
            if prev is crnt.rchild:
                prev = crnt
                if crnt.prnt:
                    crnt = crnt.prnt
                else:
                    break
            elif (prev is crnt.lchild) or (not crnt.lchild):
                print(crnt.val)
                prev = crnt
                if crnt.rchild:
                    crnt = crnt.rchild
                elif crnt.prnt:
                    crnt = crnt.prnt
                else:
                    break
            else:
                prev = crnt
                crnt = crnt.lchild

    def inorderstack(self):
        stk = []
        crnt = self.root
        while crnt or (len(stk) > 0):
            if crnt:
                # push the last node that's legit
                stk.append(crnt)
                crnt = crnt.lchild
            # crnt == None so the last node on the stack has no left child
            else: # len(stk) > 0
                    p = stk.pop()
                    print(p.val)
                    crnt = p.rchild

    def preorderstack(self):
        stk = []
        crnt = self.root
        while crnt or (len(stk) > 0):
            if crnt:
                # push the last node that's legit
                print(crnt.val)
                stk.append(crnt)
                crnt = crnt.lchild
            # crnt == None so the last node on the stack has no left child
            else: # len(stk) > 0
                    p = stk.pop()
                    crnt = p.rchild

    def postorderstack(self):
        stk = []
        stk2 = []
        crnt = self.root
        while crnt or (len(stk) > 0):
            if crnt:
                stk2 = [crnt.val] + stk2
                stk.append(crnt)
                crnt = crnt.rchild
            else: # len(stk) > 0
                    p = stk.pop()
                    crnt = p.lchild

        print(stk2)

    def preorderrec(self):
        def preorder(root):
            print(root.val)
            if root.lchild: preorder(root.lchild)
            if root.rchild: preorder(root.rchild)

        preorder(self.root)

    def postorderrec(self):
        def postorder(root):
            if root.lchild: postorder(root.lchild)
            if root.rchild: postorder(root.rchild)
            print(root.val)
        postorder(self.root)

    def inorderrec(self):
        def inorder(root):
            if root.lchild: inorder(root.lchild)
            print(root.val)
            if root.rchild: inorder(root.rchild)
        inorder(self.root)

    def __contains__(self, x):
        try:
            if self.__getitem__(x): return True
        except IndexError:
            return False

    # returns node where x would be place (ptr!=none)
    # comparisons still have to be done
    def bsttraverse(self,x):
        # prev = ptr = self.root
        # while ptr:
        #     prev = ptr
        #     if x < ptr.val:
        #         ptr = ptr.lchild
        #     elif x == ptr.val:
        #         if ptr.lchild: ptr = ptr.lchild
        #         else: return ptr
        #     else:
        #         ptr = ptr.rchild
        # return prev
        #
        prnt = ptr = self.root
        # when a len method is defined this checks the length?
        while ptr:
            prnt = ptr
            if x < ptr.val: ptr = ptr.lchild
            elif x == ptr.val: break
            else: ptr = ptr.rchild

        return ptr if ptr else prnt




    def __getitem__(self, x):
        ptr = self.bsttraverse(x)
        if ptr.val == x:
            return ptr
        else:
            raise IndexError

    def minroot(self,ptr):
        while ptr.lchild:
            ptr = ptr.lchild
        return ptr

    def min(self):
        return self.minroot(self.root)


    def maxroot(self,ptr):
        while ptr.rchild:
            ptr = ptr.rchild
        return ptr
    def max(self):
        return self.maxroot(self.root)


    def succ(self,x):

        ptr = self.bsttraverse(x)

        # this clause is ostenisbly to identify when bstraverse returns a pointer to a node that exists
        # ie we're searching for the predec of a value that exists. originally i (wrongly) assumed
        # any node that corresponds to a value which exists in the tree necessarily must have an rchild but
        # a node could come back missing a left child (which is where x belongs) but having a right child
        if ptr.rchild and x == ptr.val:
            ptr = self.minroot(ptr.rchild)
        else:
            # otherwise succ is inverse of predecessor (ie go up left and hook a right
            # if value is absent from tree and should be left child then immediately its parent satisfies ptr != ptr.prnt.rchild
            # if x should be on the left side then we need to skip and just return ptr
            if x < ptr.val:
                pass
            else:
                while ptr.prnt and ptr == ptr.prnt.rchild:
                    ptr = ptr.prnt
                ptr = ptr.prnt
        return ptr

    def predec(self,x):
        # ptr is parent
        ptr = self.bsttraverse(x)
        # this clause is ostenisbly to identify when bstraverse returns a pointer to a node that exists
        # ie we're searching for the predec of a value that exists. originally i (wrongly) assumed
        # any node that corresponds to a value which exists in the tree necessarily must have an lchild but
        # a node could come back missing a left child (which is where x belongs) but having a left child
        if ptr.lchild and x == ptr.val:
            # max left subtree
            ptr = self.maxroot(ptr.lchild)
       # go all the way to the right and make a left
        else:
            # if x should be on the right side then we need to skip and just return ptr
            if x > ptr.val:
                pass
            else:
                while ptr.prnt and ptr == ptr.prnt.lchild:
                    ptr = ptr.prnt
                ptr = ptr.prnt

        return ptr


    def _surgery(self,ex,ins):
        if not ex.prnt:
            self.root = ins
        elif ex == ex.prnt.lchild:
            ex.prnt.lchild = ins
        else: # if ex = ex.prnt.rchild
            ex.prnt.rchild = ins
        if not ins is None: ins.prnt = ex.prnt

    def delete(self,x):
        self.deleteroot(self[x])

    def deleteroot(self,nd):
        if not nd.lchild:
            x = ptr = nd.rchild
            if hasattr(ptr, 'color'):
                orig_color = ptr.color
            self._surgery(nd,x)
            self._announce()
        elif not nd.rchild:
            x = ptr = nd.lchild
            if hasattr(ptr, 'color'):
                orig_color = ptr.color
            self._surgery(nd,x)
            self._announce()
        else: # both children exist
            ptr = nd.rchild
            # find successor
            while ptr.lchild:
                ptr = ptr.lchild
            x = ptr.rchild
            # ugly hack to forward support RBtree
            if hasattr(ptr, 'color'):
                orig_color = ptr.color
            # if ptr.prnt == nd (and don't forget ptr is succesor) then the rest of the subtree
            # stretches to the right and no surgery has to be one
            if ptr.prnt == nd:
                x.prnt = ptr
            else: # if ptr.prnt != nd:
                # just puts successor's rchild into successor's position
                self._surgery(ptr,x) # still works if ptr.rchild is none
                # necessary because nd has both children and ptr isn't its right child
                self._announce()
                ptr.rchild = nd.rchild
                nd.rchild.prnt = ptr
            self._surgery(nd,ptr)
            ptr.lchild = nd.lchild
            nd.lchild.prnt = ptr
            self._announce()

        return x,ptr,orig_color

    def print(self):
        st = map(lambda x: ''.join(x),self.root.print())
        print(*st,sep='\n')
        # strr = '\n'.join(list(st))
        # return strr

if __name__ == '__main__':
    # ls = random.sample(range(100),5)
    ls = [11, 53, 35, 29, 19, 8, 6, 99, 66, 28, 45, 82, 85, 51, 2]
    b = BinarySearchTree(ls)
    # b.inorderstack()
    # r = random.sample(range(100),1)[0]
    # r = 63
    # print(sorted(ls))
    # print(r,b.succ(r))
    # print()
    # print(r,b.predec(r))
    b.print()
    while True:
        d = int(input("delete: "))
        b.delete(d)
        b.print()
# 12.1-2 minheap property says root should be larger than both of its children
