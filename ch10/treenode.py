import random
from collections import deque



class TreeNode:
    def __init__(self,val=None,prnt=None,lchild=None,rchild=None):
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
        ls = []
        if self.lchild: ls.append(self.lchild)
        if self.rchild: ls.append(self.rchild)
        return iter(ls)

    def __next__(self):
        try:
            ch = next(self.childit)
        except StopIteration:
            self.childit = iter(self.children)
            ch = next(self.childit)

        return ch

    def print(self):
        return self.pprint([],True,[])

    # basically an inorder traversal
    # really clever
    def pprint(self,pref,isTail,sb):
        if self.rchild:
            t = pref + list("│   " if isTail else "    ")
            self.rchild.pprint(t, False, sb)
        t = pref + list("└── " if isTail else "┌── ") + list(str(self.val))
        sb.append(t)
        if self.lchild:
            t = pref + list("    " if isTail else "│   ")
            self.lchild.pprint(t, True, sb)
        return sb

        # print(pref + (r"└── " if isTail else r"├── ") + str(self.val))
        # ls = list(iter(self))
        # for i in range(0,len(ls)-1):
        #     ls[i].pprint(pref + (r"    " if isTail else r"│   "), False)
        # if len(ls) > 0:
        #     ls[-1].pprint(pref + (r"    " if isTail else r"│   "), True)



# 10.4-2 depth first search
# 10.4-3 duh