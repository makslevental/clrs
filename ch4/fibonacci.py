"""
fibonacci computation clrs 4-4

consult 4-4.pdf
"""
import numpy as np
import unittest
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
    base = np.array([[1,1],[1,0]])
    if n == 0: return base[1,1]
    elif n == 1: return base[0,1]
    elif n == 2: return base[0,0]
    else: return expMatBySqrIter(base,n)[0,1]


def fibFastest(n):
    """
    use fast doubling plus unrolled matrix exponentiation

    fast doubling is simple: what's the easiest way to get to a number starting from 1
    using just double and adding one? easy to figure out if you do it in reverse: if the number is
    odd subtract one and divide by 2. repeat this recursively until you get to 1. to go in the opposite
    direction just go in the opposite direction :) binary representation helps: 19 = 10011.
    subtract 1 and divide by 2 = 1001 = 9, subtract 1 and divide by 2 = 100 = 4, divide by 2 = 10 = 2, divide by 2 = 1
    to go in the other direction just reverse the steps: 0 (*2),0(*2),1(*2 +1),1(*2 +1).
    :param n:
    :return:
    """

    # get the binary rep of the index of the fib sequence
    bn = bin(n)[3:]
    f_k = f_kp1 = 1
    f_2k = f_2kp1 = 1
    k = 1
    while k < n:
        if bn[0] == '0':
            # just double (i.e. do the steps to get the f_2k and f_2kth_plus_one terms of the sequence)
            f_2k = f_k*(2*f_kp1 - f_k)
            f_2kp1 = (f_kp1)**2 + f_k**2
            f_k, f_kp1 = f_2k, f_2kp1
            k *= 2
            # move on to next bit in bin rep
            bn = bn[1:]
        elif bn[0] == '1':
            # double and add 1 (i.e. do the process to get the next term in the fib sequence, i.e. f_2k_plus_two -
            # this is just updating using the regular fib rule)
            f_2k = f_k*(2*f_kp1 - f_k)
            f_2kp1 = (f_kp1)**2 + f_k**2
            f_2kp1, f_2k = f_2k + f_2kp1, f_2kp1
            f_kp1, f_k = f_2kp1, f_2k

            k *= 2
            k += 1
            bn = bn[1:]

    return f_k


class FibTest(unittest.TestCase):

    fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377,
            610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657,
            46368, 75025, 121393, 196418, 317811, 514229, 832040,
            1346269, 2178309, 3524578, 5702887, 9227465, 14930352,
            24157817, 39088169]

    def testNthTerm(self):
        for k,f in enumerate(self.fibs,start=1):
            try:
                f1 = fibRecSlowest(k)
                f2 = fibRecSlow(k)
                f3 = fibFastest(k)
                f4 = fibFastest(k)
                self.assertTrue(f1 == f2 == f3 == f4 == f)
            except AssertionError as a:
                print(f1, f2, f3, f4)

if __name__ == '__main__':
    unittest.main()
