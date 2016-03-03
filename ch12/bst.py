from ch10.binary_tree import TreeNode
import random
class BinarySearchTree:
    def __init__(self,ls=None):
        self.root = TreeNode()
        if ls:
            self.ls = ls
            self.root.val = ls[0]
            for v in ls[1:]:
                self.insert(v)

    # i want leaves to have nones as children
    def insert(self,x):
        if not self.root.val:
            self.root.val = x
        else:
            prnt = nxtnode = self.root
            while True:
                prnt = nxtnode
                if x <= nxtnode.val:
                    nxtnode = nxtnode.lchild
                    if not nxtnode:
                        prnt.lchild = TreeNode(x,prnt)
                        break
                elif x > nxtnode.val:
                    nxtnode = nxtnode.rchild
                    if not nxtnode:
                        prnt.rchild = TreeNode(x,prnt)
                        break


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

    # TODO doesn't work
    def postorderstack(self):
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
                    crnt = p.rchild



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





if __name__ == '__main__':
    b = BinarySearchTree(random.sample(range(100),3))
    print('preorder stack')
    b.preorderstack()
    print('preorder rec')
    b.preorderrec()
    print('postorder stack')
    b.postorderstack()
    print('postorder rec')
    b.postorderrec()
    print('inorder stack')
    b.inorderstack()
    print('inorder rec')
    b.inorderrec()

# 12.1-2 minheap property says root should be larger than both of its children
