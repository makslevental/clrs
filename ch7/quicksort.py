import numpy as np


def quick_sort_hard(ls):
    np.random.shuffle(ls)
    return _quick_sort_hard(ls,0,len(ls)-1)

def quick_sort_easy(ls):
    np.random.shuffle(ls)
    return _quick_sort_easy(ls)

def _quick_sort_hard(ls,lo,hi):
    if lo < hi:
        if hi-lo+1 == 2:
            ls[lo],ls[hi] = min(ls[lo],ls[hi]),max(ls[lo],ls[hi])
            return
        p = partition(ls,lo,hi)
        _quick_sort_hard(ls,lo,p-1)
        _quick_sort_hard(ls,p+1,hi)

def partition(ls,lo,hi):
    mid = (lo+hi)//2
    l,m,h = ls[lo],ls[mid],ls[hi]
    if (l <= m <= h) or (l >= m >= h):
        medi = mid
    elif (m <= l <= h) or (h <= l <= m):
        medi = lo
    else:
        medi = hi

    # place for swapping. i marks the end of the less than part of the array

    piv = ls[medi]
    ls[hi],ls[medi] = ls[medi],ls[hi]
    i = lo
    if ls[i] <= piv: i += 1
    for j in range(lo+1,hi):
        if ls[j] <= piv:
            ls[i],ls[j] = ls[j],ls[i]
            i += 1
        # after the loop is done ls[j] is always >= the pivot
        # since ls[i] is always >= the pivot
    ls[i],ls[hi] = ls[hi],ls[i]
    return i




def _quick_sort_easy(ls):
    ls = ls[:]
    if len(ls) <= 1: return ls
    if len(ls) == 2: return [min(ls),max(ls)]

    if (ls[0] <= ls[len(ls)//2] <= ls[-1]) or (ls[0] >= ls[len(ls)//2] >= ls[-1]):
        medi = len(ls)//2
    elif (ls[len(ls)//2] <= ls[0] <= ls[-1]) or (ls[-1] >= ls[0] >= ls[len(ls)//2]):
        medi = 0
    else:
        medi = -1
    t = ls[medi]
    del ls[medi]
    left = [x for x in ls if x < t]
    right = [x for x in ls if x >= t]

    left = _quick_sort_easy(left)
    right = _quick_sort_easy(right)
    return left+[t]+right


if __name__ == '__main__':
    try:
        for i in range(1000):
            ls = list(np.random.randint(1,10000,10))
            temp = ls[:]
            #ls = [4110, 4315, 3124, 1251, 1744, 3009, 7243, 5785, 5785, 4952]
            quick_sort(ls)
            assert np.array_equal(sorted(ls),ls)
    except AssertionError:
        print(temp,ls,sorted(ls),sep='\n')
        raise
