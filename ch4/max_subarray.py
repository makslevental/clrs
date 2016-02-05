import numpy as np
import operator
import unittest



def kadanes_subarray(arr):
    """
    kadane's linear time algorithm for finding max subarray.
    walk from left to right adding each entry and keeping track
    of maximum so far. if ever the sum drop belows zero then we
    don't care about that bit of the array (clearly this doesn't work
    for largest sum of all negative numbers, in which case you'd just find minimum).
    not caring means we can start counting the left bound
    :param arr: any array
    :return: (maximum sum subarray, maximum sum)
    """
    sum_ending_here = max_so_far = 0
    max_left_bound = max_right_bound = current_left_bound = current_right_bound = 0
    for i in range(len(arr)):
        if sum_ending_here + arr[i] > 0:
            sum_ending_here += arr[i]
            current_right_bound = i
        else:
            # reset sum since every contiguous sum before
            # this i is nonpositive
            sum_ending_here = 0
            # if we're in this branch then arr[i] is obviously negative
            # and the sum should start (at best) at i+1
            # -- this is wrong but worked. arr[i] could be positive and the sum
            # had just been negative and greater than that positive entry but
            # current_left_bound = current_right_bound = i
            # is wrong too because if arr[i]<0 but arr[i]>0 and sum + arr[i] > 0
            # then the left bound isn't updated. so
            current_left_bound = current_right_bound = i+1
            # is correct after all because if

        if sum_ending_here >= max_so_far:
            # max_left_bound = current_left_bound
            max_so_far = sum_ending_here
            max_right_bound = current_right_bound
            max_left_bound = current_left_bound

    return (np.array(arr[max_left_bound:max_right_bound+1]),max_so_far)


def max_subarray_nlgn(arr):
    """
    divide and conquer solution for the maximum sum subarray problem.
    let m=len(arr)/2. find the maximum sum subarray in the left half (array left of m),
    find the maximum sum subarray in the right half (array right of m), find the maximum sum subarray
    crossing the middle by fanning out to the left of m, and to the right of m just summing linearly

    not stable against several subarray sums being equal (i.e. zero prefix or suffix)

    :param arr: any array
    :return: (maximum sum subarray, maximum sum)
    """

    # base case of divide and conquer
    if len(arr) == 1:
        return arr,arr[0]

    # // for rounding in python3
    mid = len(arr)//2
    lharr = arr[0:mid]
    rharr = arr[mid:]
    maxSubL, maxSubSumL = max_subarray_nlgn(lharr)
    maxSubR, maxSubSumR = max_subarray_nlgn(rharr)

    i = crsSubLBound = len(lharr)-1
    crsLSubMaxSum = sum = lharr[i]
    # reverse range
    for i in range(len(lharr)-2,-1,-1):
        sum += lharr[i]
        if sum >= crsLSubMaxSum:
            crsLSubMaxSum = sum
            crsSubLBound = i

    i = crsSubRBound = 0
    crsRSubMaxSum = sum = rharr[i]


    for i,v in enumerate(rharr[1:]):
        sum += v
        if sum >= crsRSubMaxSum:
            crsRSubMaxSum = sum
            # the enumeration always starts from 0
            crsSubRBound = i+1

    max_cross_sum = crsRSubMaxSum+crsLSubMaxSum
    max_cross_arr = np.concatenate([lharr[crsSubLBound:],rharr[:crsSubRBound+1]])
    return max([(maxSubL,maxSubSumL), (maxSubR,maxSubSumR), (max_cross_arr,max_cross_sum)], key=operator.itemgetter(1))


def bruteforce(arr):
    test_mat = np.zeros((len(arr),len(arr)))
    for i in range(len(arr)):
        for j in range(i,len(arr)):
            test_mat[i,j] = np.sum(arr[i:j+1])
    inds = np.unravel_index(test_mat.argmax(),test_mat.shape)
    goldstnrd = arr[inds[0]:inds[1]+1]
    return goldstnrd,goldstnrd.sum()

class RandomArrays(unittest.TestCase):
    def testRandomArrays(self):
        for i in range(1000):
            arr = np.random.randint(low=-100,high=100, size=10)

            goldstnrd =  bruteforce(arr)[0]
            divconq = max_subarray_nlgn(arr)[0]
            kadane = kadanes_subarray(arr)[0]
            try:
                self.assertTrue(np.array_equal(goldstnrd,divconq))
                self.assertTrue(np.array_equal(divconq,kadane))
            except AssertionError as a:
                print(arr,(goldstnrd,goldstnrd.sum()),(divconq,divconq.sum()),(kadane,kadane.sum()),sep='\n')
                raise AssertionError




if __name__ == '__main__':
    unittest.main()
    # print(max_subarray_nlgn([-92,  69, -88, -55,  95  ,59  ,59  ,89 ,-20 ,-83]))
    # exercise 4.1-1: what does max_subarray_lgn return when all of the entries are negative?
    # the smallest negative number i think
    # arr = np.random.randint(low=-100,high=-1, size=10)
    # print(arr,max_subarray_nlgn(arr))
    # whoops my implementation initializes tot to zero. if i set it to be the first entry it will probably
    # as i expected. oh well it turns out to be inelegant to modify to return the smallest number. i need
    # to do the loop check outside the loop in order to update max blah blah blah. checked and it works.

    # exercise 4.1-2: write pseudocode for bruteforce
    # appears in unittest

    # exercise 4.1-3: figure out when bruteforce is faster than recursive and then use the bruteforce for smaller n than that.
    # good excuse to use timeit module
    # import timeit
    #
    # setup = '''import numpy as np; from __main__ import max_subarray_nlgn, bruteforce; '''
    # for i in range(1,100):
    #     print(i,min(timeit.repeat('''arr = np.random.randint(low=-100,high=100, size={size}); max_subarray_nlgn(arr)'''.format(size=i), setup=setup, repeat=7, number=100))
    #             ,min(timeit.repeat('''arr = np.random.randint(low=-100,high=100, size={size}); bruteforce(arr)'''.format(size=i), setup=setup, repeat=7, number=100)))

    """
    results are :
    1 0.000729504998162156 0.005452118002722273
    2 0.004974385999958031 0.008375998000701657
    3 0.00895411400051671 0.012647072999243392
    4 0.012894096998934401 0.018120706001354847
    5 0.017049484002200188 0.024843573999532964
    6 0.0208599219986354 0.012904609000543132
    7 0.010756185001810081 0.0421681659972819
    8 0.02900555299856933 0.05256015100167133
    9 0.0332181749981828 0.06526233999829856
    10 0.03702341900134343 0.07842945000084
    11 0.041197393999027554 0.09191363999707391
    12 0.039867478000815026 0.04411568899740814
    13 0.05029373200159171 0.1276224950015603

    looks like recursive function is always faster? what i really need to do is turn the tail call recursion into a for loop
    """

    # 4.1-4 skip
    # 4.1-5 kadane's algorithm... or not? it's not. it's different but close?
    # a maximum subarray ENDING at j+1 of A[1..j+1] includes the maximum subarray of A[1..j+1]
    # so if the indices of the maximum subarray of A[1..j+1] are i,i' then the maximum subarray ENDING at
    # j+1 is A[i,j+1]. Why? Well clearly A[i,j+1] ends at j+1 and it's maximal because sum(A[i,i']) > sum(A[j',i'])
    # for any j' (definition of maximum subarray). i.e. it makes sense to include the chunk of A[1..j+1] that has
    # the greatest sum in order to maximize the array ending at j+1. if you know the maximum subarray ENDING at j+1
    # then the maximum subarray ENDING at j+2 is either A[i,j+2] or A[j+2]. why? if sum(A[i,j+1]) is negative and
    # A[j+2] is positive then clearly we should just throw out A[i,j+2]. if sum(A[i,j+1]) is negative and A[j+1] is negative
    # then similarly you should just throw away the negative causing A[i,j+2]. if sum(A[i,j+1]) is positive and A[j+2] is negative
    # then we should keep A[i,j+1] to counteract the negativity of A[j+2]. If both are positive then we should definitely keep
    # A[i,j+1]. if it's any of the cases where we throw out A[i,j+1] then we have a candidate for a new maximum subarray
    # for the entire array: if A[j+2] is greater than sum(A[i,j+2]) then we should start considering subarrays
    # starting at j+2 instead of i.
    #
    # much simpler expanation:
    # Idea: Do a simple scan, maintaining two values along the way, for index i:
    # "maxhere" : maximum subarray of A[0..i] of those ending precisely at i
    # "maxsofar" : maximum subarray of A[0..i]
    #
    # why does this work? maxhere == my max_ending_here is the max subbarray OF A[0..i] ending HERE.
    # the maximum subarray of A[0..i] is the max subarray of A[0..i'] ending at some i', so i can restrict my set
    # of considered subarrays to be these, i.e. max subarrays of A[0..i'] ending at i' for all i'. this is the key!
    # restate the problem in a way where there is "optimal substructure". this takes creativity duh. now the question
    # becomes how to update max subarray of A[0..i+1] ending at i+1 given knowledge of max subarray of A[0..i] ending at i
    # answer: above. the max subarray of A[0..i+1] ending at i+1 is either the max subarray of A[0..i] ending at i is
    # with A[i+1] concatenated or just A[i+1].
    #