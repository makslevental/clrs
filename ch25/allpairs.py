import numpy as np

def extend(L,W):
    Lp = np.full_like(L, np.inf)
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

if __name__ == '__main__':
    A = np.ones((10,10))
    B = np.full_like(A,5)
    C = extend(A,B)
    print(C)


# 25.1-5

# 25.1-6

# 25.1-7

# 25.1-9 look for negatives on the diagonal

# 25.1-10 negatives on the diagonal (whenever they show up first  in L^m) is the length.