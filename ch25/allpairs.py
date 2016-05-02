import numpy as np

def extend(L,W):
    Lp = np.full_like(L, np.inf)
    for i in range(L.shape[0]):
        L[i,i] = 0

    for i in range(L.shape[0]):
        for j in range(L.shape[1]):
            Lp[i,j] = min(L[i,:]+W[:,j])

    return Lp


def allpairs(W):

    n = W.shape[0]

    Wp = np.zeros_like(W)
    y = np.zeros_like(W)
    # this works bottom up instead of top down
    while n > 1:
        if n%2 == 0: Wp,n = extend(Wp,Wp), n/2
        # if n is odd then we need to do "slide" out 1 copy of the current x
        # because we'll be missing that many at the end since we're
        # setting n=(n-1)/2
        else: y,Wp,n = extend(Wp,y), extend(Wp,Wp), (n-1)/2
    return extend(Wp,y)


def floydwarshall(W):
    n = W.shape[0]

    Dk_1 = W

    for k in range(n):
        Dk = np.full_like(W,np.inf)
        for i in range(n):
            for j in range(n):
                # either k is not an intermediate vertex of the shortest path
                # from i to j or k is and then the shortest path
                # from i to j is the path from i to k and then k to j
                Dk[i,j] = min(Dk_1[i,j],Dk_1[i,k]+Dk_1[k,j])
        Dk_1 = Dk

    return Dk

def trans_closure(W):
    n = W.shape[0]

    Tk_1 = W.full_like(W,False)
    for i in range(n):
        for j in range(n):
            if (not W[i,j] is np.inf and W[i,j] > 0) or i == j:
                Tk_1[i,j] = True

    for k in range(n):
        Tk = np.full_like(W,False)
        for i in range(n):
            for j in range(n):
                Tk = Tk_1[i,j] or (Tk_1[i,k] and Tk_1[k,j])
        Tk_1 = Tk

    return Tk

def findpi(L,W):
    n = L.shape[0]
    pi = np.full_like(L,None)
    for i in range(n):
        for j in range(n):
            # guess and check
            for k in range(n):
                if L[i,k] + W[k,j] == L[i,j]:
                    pi[i,j] = k


if __name__ == '__main__':
    A = np.ones((10,10))
    B = np.full_like(A,5)
    C = extend(A,B)
    print(C)


# 25.1-5

# 25.1-6 dumbest shit: loop over everything and check against edge weights to see shortest path
# between two vertices is edge weight plus shortest path to first vertex

# 25.1-7

# 25.1-9 look for negatives on the diagonal

# 25.1-10 negatives on the diagonal (whenever they show up first  in L^m) is the length.