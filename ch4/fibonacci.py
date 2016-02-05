"""
fibonacci computation clrs 4-4

consult 4-4.pdf
"""
import numpy as np

def fibRecSlowest(n):
    """
    slow recursive implementation for computing fibonacci numbers
    :param n:
    :return:
    """
    if n == 1 or n == 2:
        return 1
    else:
        return fibRecSlowest(n-1) + fibRecSlowest(n-2)

def fibRecSlow(n):
    if n == 1 or n == 2:
        return 1
    nthterm = 1
    nplus1thterm = 1
    i = 3
    while i<=n:
        nplus1thterm, nthterm = nthterm + nplus1thterm, nplus1thterm
        i+=1

    return nplus1thterm

def expNumBySqrRec(x, n):
    """
    exponentiation by squaring for numbers
    :param x:
    :param n:
    :return:
    """
    if n < 0: return expNumBySqrRec(1 / x, -n)
    elif n == 0 : return 1
    elif n == 1 : return x
    elif n%2 == 1: return x * expNumBySqrRec(x ** 2, (n - 1) / 2)
    elif n%2 == 0: return expNumBySqrRec(x ** 2, n / 2)


def expNumBySqrIter(x, n):
    """
    exponentiation by squaring for numbers
    :param x:
    :param n:
    :return:
    """
    if n < 0: x,n = 1/x, -n
    elif n == 0 : return 1
    y = 1
    # this works bottom up instead of top down
    while n > 1:
        if n%2 == 0: x,n = x**2, n/2
        # if n is odd then we need to do "slide" out 1 copy of the current x
        # because we'll be missing that many at the end since we're
        # setting n=(n-1)/2
        else: y,x,n = x*y,x**2,(n-1)/2
    return x*y


def expMatBySqrIter(x, n):
    """
    exponentiation by squaring for numbers
    :param x:
    :param n:
    :return:
    """
    if n < 0: x,n = np.linalg.inv(x), -n
    elif n == 0 : return np.eye(x.shape[0], dtype=int)
    y = np.eye(x.shape[0], dtype=int)
    # this works bottom up instead of top down
    while n > 1:
        if n%2 == 0: x,n = np.dot(x,x), n/2
        # if n is odd then we need to do "slide" out 1 copy of the current x
        # because we'll be missing that many at the end since we're
        # setting n=(n-1)/2
        else: y,x,n = np.dot(x,y),np.dot(x,x),(n-1)/2
    return np.dot(x,y)


def expMatBySqrRec(x, n):
    """
    exponentiation by squaring for matrices
    :param x:
    :param n:
    :return:
    """
    if n < 0: return expMatBySqrRec(np.linalg.inv(x), -n)
    elif n == 0 : return np.eye(x.shape[0], dtype=int)
    elif n == 1 : return x
    elif n%2 == 1: return np.dot(x,expMatBySqrRec(np.dot(x,x), (n - 1) / 2))
    elif n%2 == 0: return expMatBySqrRec(np.dot(x,x), n / 2)


def fibExpBySqrRecFast(n):
    pass

if __name__ == '__main__':
    # print(fibRecSlow(10))
    print(expMatBySqrRec(2,10))