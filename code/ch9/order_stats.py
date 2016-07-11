import numpy as np
from collections import defaultdict

def min_max(ls):
    temp = ls[:]
    lls = len(ls)
    minn,maxx = temp[0],temp[0]
    if lls%2 == 1:
        temp = [None]+temp

    for i in range(2,lls,2):
            lmin,lmax = (temp[i],temp[i+1]) if temp[i] <= temp[i+1] else (temp[i+1],temp[i])
            maxx = maxx if maxx >= lmax else lmax
            minn = minn if minn <= lmin else lmin
    #
    # if lls%2 == 0:
    #     minn,maxx = (ls[0],ls[1]) if ls[0] < ls[1] else (ls[1],ls[0])
    #     for i in range(2,lls,2):
    #         # if ls[i] < ls[i+1] then -(ls[i] < ls[i+1]) is all 1s
    #         # and temp = (ls[i] ^ ls[i+1])
    #         # else it's all zeros
    #         # temp = (ls[i] ^ ls[i+1]) & -(ls[i] < ls[i+1])
    #         # if temp = (ls[i] ^ ls[i+1]), i.e. ls[i] < ls[i+1]
    #         # then ls[i+1] ^ ls[i] ^ ls[i+1] = ls[i]
    #         # else if temp = 0 then lmin = ls[i+1]
    #         # lmin = ls[i+1] ^ temp
    #         # if temp = 0, i.e ls[i]>= ls[i+1] then ls[i] ^ 0 = ls[i]
    #         # else if temp = (ls[i] ^ ls[i+1]), i.e. ls[i] < ls[i+1]
    #         # then lmax = ls[i] ^ ls[i] ^ ls[i+1] = ls[i+1]
    #         # lmax = ls[i] ^ temp
    #         lmin,lmax = (ls[i],ls[i+1]) if ls[0] <= ls[1] else (ls[i+1],ls[i])
    #         maxx = maxx if maxx >= lmax else lmax
    #         minn = minn if minn <= lmin else lmin
    #         # if maxx < lmax then -(maxx<lmax) is all 1s (-1 is all 1s in twos complement)
    #         # then ((maxx ^ lmax) & 111) = maxx ^ lmax and therefore lmax ^ maxx ^ lmax = maxx
    #         # if maxx >= lmax then -(maxx<lmax) is all zeros and the whole parens disappears
    #         # maxx = maxx ^ ((maxx ^ lmax) & -(maxx < lmax))
    #         # if minn < lmin then -(minn < lmin) is all 1s and we have lmin ^ minn ^ lmin = minn
    #         # if minn >= lmin then -(minn < lmin) is 0 and we have lmin
    #         # minn = lmin ^ ((minn ^ lmin) & -(minn < lmin))
    # else:
    #     minn,maxx = ls[0],ls[0]
    #     for i in range(1,lls,2):
    #         lmin,lmax = (ls[i],ls[i+1]) if ls[0] <= ls[1] else (ls[i+1],ls[i])
    #         maxx = maxx if maxx >= lmax else lmax
    #         minn = minn if minn <= lmin else lmin
    #         # if maxx < lmax then -(maxx<lmax) is all 1s (-1 is all 1s in twos complement)
    #         # then ((maxx ^ lmax) & 111) = maxx ^ lmax and therefore lmax ^ maxx ^ lmax = maxx
    #         # if maxx >= lmax then -(maxx<lmax) is all zeros and the whole parens disappears
    #         # maxx = maxx ^ ((maxx ^ lmax) & -(maxx < lmax))
    #         # if minn < lmin then -(minn < lmin) is all 1s and we have lmin ^ minn ^ lmin = minn
    #         # if minn >= lmin then -(minn < lmin) is 0 and we have lmin
    #         # minn = lmin ^ ((minn ^ lmin) & -(minn < lmin))

    return minn,maxx

# use elimination but keep track of each person the winner beat
def min_and_second_min(ls):
    d = defaultdict(list)
    temp = ls[:]
    while len(temp) > 1:
        ltemp = []
        if len(temp)%2 == 1:
            temp = [np.inf]+temp

        for i in range(0,len(temp),2):
            d[temp[i]].append(temp[i+1])
            d[temp[i+1]].append(temp[i])
            ltemp.append(temp[i] if temp[i] < temp[i+1] else temp[i+1])

        temp = ltemp

    min = temp[0]
    temp = [x for x in d[min] if x != np.inf]

    while len(temp) > 1:
        ltemp = []
        if len(temp)%2 == 1:
            temp = [np.inf]+temp

        for i in range(0,len(temp),2):
            ltemp.append(temp[i] if temp[i] < temp[i+1] else temp[i+1])

        temp = ltemp

    return min,temp[0]


def randompartition(ls,lo,hi):
    r = np.random.randint(lo,hi+1)
    ls[hi],ls[r] = ls[r],ls[hi]

    p = ls[hi]
    i = lo
    if ls[i] < p:
        i +=1

    for j in range(lo+1,hi):
        if ls[j] < p:
            ls[j], ls[i] = ls[i], ls[j]
            i +=1

    ls[hi], ls[i] = ls[i], ls[hi]
    # returns the exact index of the pivot
    return i

def orderstat(ls,lo,hi,i):
    if lo == hi:
        return ls[lo]
    # q is the exact index of the pivot, so the number at position q is in its proper place.
    # mind the fact that order statistics start from 1 but in here they start from 0
    q = randompartition(ls,lo,hi)
    k = q-lo+1 # which order statistic ls[q] is
    if i == k:
        return ls[q]
    elif i < k:
        # if in the left half then ith order statistic is still in ith place on the left
        return orderstat(ls,lo,q-1,i) # similar to bst something something something
    else:
        return orderstat(ls,q+1,hi,i-k) # ith order stat on the right is actually i-k from the front on the right


if __name__ == '__main__':

    ls = list(set(np.random.randint(1,100,np.random.randint(10,20))))
    np.random.shuffle(ls)
    ls = list(ls)
    # ls = list(range(100,1,-1))
    # a,b = min_max(ls)
    # print(min(ls),max(ls),a,b)
    # ls = [42, 1, 97, 98, 22, 17, 48, 29, 94, 67, 86, 34]
    # a,b = min_and_second_min(ls)
    # print(sorted(ls)[:2],a,b)
    for i,v in enumerate(sorted(ls)):
        # i+1 because what's a 0th order statistic anyway?
        o = orderstat(ls,0,len(ls)-1,i+1)
        print(i,v)
        assert v == o

# 9.1-1 tournament style to determine min: compare all pairs: n/2, compare all winners of that: n/4, etc, until you
# two competitors

# 9.3-5 essentially use binary search

# 9.3-6 if k is even then there are k-1 (and odd number) of desired pivots and one of them is the median. find the median
# and partition and solved the 2*n/2 sub problems. if k is odd be more careful :)

# 9.3-7 find the median, then subtract from everything then find the kth order statistic

# 9.3-8 the median always between the two medians (which can found computed in constant). if the medians are equal then
# return the median. otherwise recurse into the left side of right side of each array (depending on which median is larger
# than which) and check again if medians are equal.

# 9.3-9 the median minimizes the sum distances by definition.

# 9-2a duh

# 9-2b sort then sum weights until you exceed 1/2

# 9-2c find the median and (and by virtue partition around it). compute the total weight in the lower half. if requirements
#  are met the return m. if total weight is less than w=1/2 then the solution is on the left side, else it's on the right.
# recurse while "intelligently" updating the weight you're looking for

# 9-2d  duh

# 9-2e  since the directions are completely decoupled use median in each direction.