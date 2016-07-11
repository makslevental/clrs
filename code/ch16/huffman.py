from ch10.treenode import TreeNode
from queue import PriorityQueue
import itertools
from math import sqrt
import string
from random import sample

def fib(n):
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))

class HuffNode(TreeNode):
    def __init__(self,freq=0,**kwargs):
        super().__init__(**kwargs)
        self.freq = freq

class HuffTree():
    def __init__(self,chars):
        q = PriorityQueue()
        counter = itertools.count() # unique sequence count
        for freq,char in chars:
            q._put((freq,(next(counter),HuffNode(freq=freq,val=char))))

        for _ in range(len(chars)-1):
            left = q._get()
            right = q._get()
            freq = left[0] + right[0]
            z = HuffNode(freq=freq,lchild=left[1][1],rchild=right[1][1])
            z.lchild.prnt = z.rchild.prnt = z
            q._put((freq,(next(counter),z)))

        self.root = q._get()[1][1]
        self.codes_dict = self._codes()

    def _codes(self):
        # push the last good one
        prev = crnt = self.root
        code = []
        codes = []
        while crnt is not None:
            if crnt == prev.prnt:
                code.pop()
                if prev == crnt.lchild:
                    code.append(1)
                    prev = crnt
                    crnt = crnt.rchild
                elif prev == crnt.rchild:
                    prev = crnt
                    crnt = crnt.prnt
            else:
                prev = crnt
                if crnt.lchild is not None:
                    code.append(0)
                    crnt = crnt.lchild
                elif crnt.rchild is not None:
                    code.append(1)
                    crnt = crnt.rchild
                else:
                    codes.append((crnt.val,''.join(str(c) for c in code[:])))
                    crnt = crnt.prnt

        return dict(codes+[(' ', ' ')])

    def encode(self,text):
        return ''.join([self.codes_dict[t] for t in text])

    def decode(self,cypher):

        word = []
        i = 0
        ptr = self.root
        while i < len(cypher):
            if cypher[i] == '0':
                if ptr.lchild is not None:
                    ptr = ptr.lchild
                    i += 1
                else:
                    word.append(ptr.val)
                    ptr = self.root
            elif cypher[i] == '1':
                if ptr.rchild is not None:
                    ptr = ptr.rchild
                    i += 1
                else:
                    word.append(ptr.val)
                    ptr = self.root
        word.append(ptr.val)
        return word

    def print(self):
        st = map(lambda x: ''.join(x),self.root.print())
        print(*st,sep='\n')




if __name__ == '__main__':
    chars = [(1, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (5, 'e'), (8, 'f'), (13, 'g'), (21, 'h')]
    chars = list(zip([fib(n) for n in range(len(string.ascii_lowercase))],string.ascii_lowercase))
    h = HuffTree(chars)
    print(h.codes_dict)
    print(h.encode('abcdef'))
    print(h.decode(h.encode('abcdef')))
    h.print()


