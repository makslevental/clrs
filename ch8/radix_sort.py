import numpy as np


class Num:
    def __init__(self,x,parent):
        self.parent = parent
        self.n = x

    def __str__(self):
        return str(self.n)


class LstNums:
    """
    eg = [[Num(1),Num(2),Num(2)],[Num(4),Num(5),Num(6)],[Num(7),Num(8),Num(9)]] == [123,456,789]
    """
    def __init__(self,ls):
        self.back = []
        for x in ls:
            self.back.append(Num(x,self))

    def __getitem__(self, item):
        return self.back[item]

    def __str__(self):
        return ''.join(list(map(lambda x:str(x.n),self.back)))

    def __eq__(self, other):
        return int(self.__str__()) == other

    def __int__(self):
        return int(self.__str__())


def counting_sort_backwards_lstnums(lsts,d):
    #lsts is a list lstnums, d is the digit we're interested in sorting on
    k = max(map(lambda x: x[d].n,lsts))
    # +1 so that as if 1 indexing instead of 0 indexing
    c = (k+1)*[0]
    for ls in lsts:
        c[ls[d].n] += 1

    # c[i] is now the number occurrences of i
    for i in range(1,k+1):
        c[i] = c[i-1] + c[i]

    # c[i] is now the number of elements in the original list less or equal
    # to i
    b = len(lsts)*[None]

    # this makes counting sort stable
    # traverse in reverse order because the count places the entry
    # into its last appearing position. in order forwards you'd have
    # count the number of elements /ahead/.
    for i in range(len(lsts)-1,-1,-1):
        # e is a Num - it is the dth digit
        e = lsts[i][d]
        b[c[e.n]-1] = e.parent
        c[e.n] -= 1

    return b


def radix_sort(ls):
    d = [list(map(int,str(x))) for x in ls]
    max_len = max(map(len,d))
    d = [(max_len-len(x))*[0]+x for x in d]
    d = [LstNums(x) for x in d]
    b = counting_sort_backwards_lstnums(d,-1)
    for i in range(-2,-max_len-1,-1):
        b = counting_sort_backwards_lstnums(b,i)

    return b

if __name__ == '__main__':
    ls = np.random.randint(1,100000000,10)
    print(*ls,sep='\n')
    print()
    d = radix_sort(ls)
    print(*d,sep='\n')
    print()

# 8.3-4 use base n

# 8.4-4

# 8.4-5 Y=F(X) is always uniformly distributed

# 8-4 use quicksort but use the red jug for pivoting blue jugs and the blue jug for pivoting red jugs
