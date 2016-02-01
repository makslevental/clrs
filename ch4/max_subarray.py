import numpy as np
import operator

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
    tot = 0
    # reverse range
    for i in range(len(left_half_arr)-1,-1,-1):
        tot += left_half_arr[i]
        if tot >= left_crs_max:
            left_crs_max = tot
            crs_left_bound = i

    tot = 0
    for i in range(len(right_half_arr)):
        tot += right_half_arr[i]
        if tot >= right_crs_max:
            right_crs_max = tot
            crs_right_bound = i

    max_cross = left_crs_max+right_crs_max
    return max([(max_subarr_left_arr,max_subarr_left_arr_tot),
                (max_subarr_right_arr,max_subarr_right_arr_tot),
                (np.concatenate([left_half_arr[crs_left_bound:],right_half_arr[:crs_right_bound+1]]),max_cross)],
               key=operator.itemgetter(1))

if __name__ == '__main__':

    for i in range(1000):
        arr = np.random.randint(low=-100,high=100, size=20)
        test_mat = np.zeros((len(arr),len(arr)))
        for i in range(len(arr)):
            for j in range(i,len(arr)):
                test_mat[i,j] = np.sum(arr[i:j+1])

        inds = np.unravel_index(test_mat.argmax(),test_mat.shape)
        if not (np.array_equal(arr[inds[0]:inds[1]+1],max_subarray_nlgn(arr)[0]) and \
                 np.array_equal(kadanes_subarray(arr)[0],max_subarray_nlgn(arr)[0])):
            print((arr[inds[0]:inds[1]+1],arr[inds[0]:inds[1]+1].sum()))
            print(max_subarray_nlgn(arr))
            print(kadanes_subarray(arr)[0],kadanes_subarray(arr)[0].sum())

