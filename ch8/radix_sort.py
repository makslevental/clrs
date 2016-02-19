import numpy as np
class Num():
    def __init__(self,x,parent):
        self.parent = parent
        self.n = x




class LstNums():
    def __init__(self,ls):
        self.back = []
        for x in ls:
            self.back.append(Num(x,self))

    def __getitem__(self, item):
        return self.back[item]

    def __str__(self):
        return ''.join(list(map(lambda x:str(x.n),self.back)))



def counting_sort_backwards_lstnums(lsts,d):
    #lsts is a list lstnums
    k = max(map(lambda x: x[d].n,lsts))
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

    for x in b:
        print(x)


if __name__ == '__main__':
    ls = np.random.randint(1,100000000,10)
    print(*ls,sep='\n')
    d = radix_sort(ls)
    print(*d,sep='\n')
