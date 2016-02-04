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
    midpoint = len(arr)//2
    left_half_arr = arr[0:midpoint]
    right_half_arr = arr[midpoint:]
    max_subarr_left_arr, max_subarr_left_arr_tot = max_subarray_nlgn(left_half_arr)
    max_subarr_right_arr, max_subarr_right_arr_tot = max_subarray_nlgn(right_half_arr)

    crs_right_bound = crs_left_bound = None
    right_crs_max = left_crs_max = -np.inf
    tot = left_half_arr[-1]
    # reverse range
    i = 0
    for i in range(len(left_half_arr)-2,-1,-1):
        tot += left_half_arr[i]
        if tot >= left_crs_max:
            left_crs_max = tot
            crs_left_bound = i

    if tot >= left_crs_max:
        left_crs_max = tot
        crs_left_bound = i

    tot = right_half_arr[0]
    # for i,v in enumerate(right_half_arr[1:]):
    #     tot += v
    #     if tot >= right_crs_max:
    #         right_crs_max = tot
    #         crs_right_bound = i
    for i in range(1,len(right_half_arr)):
        tot += right_half_arr[i]
        if tot >= right_crs_max:
            right_crs_max = tot
            # i'm dumb. how the hell did this ever work? this gives me a relative index
            crs_right_bound = i
    if tot >= right_crs_max:
        right_crs_max = tot
        # i'm dumb. how the hell did this ever work? this gives me a relative index
        crs_right_bound = i

    max_cross = left_crs_max+right_crs_max
    return max([(max_subarr_left_arr,max_subarr_left_arr_tot),
                (max_subarr_right_arr,max_subarr_right_arr_tot),
                (np.concatenate([left_half_arr[crs_left_bound:],right_half_arr[:crs_right_bound+1]]),max_cross)],
               key=operator.itemgetter(1))


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
    # unittest.main()
    print(max_subarray_nlgn([-92,  69, -88, -55,  95  ,59  ,59  ,89 ,-20 ,-83]))
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
    # 4.1-5 kadane's algorithm... or not? it's not. it's different