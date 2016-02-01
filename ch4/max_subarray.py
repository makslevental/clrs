import numpy as np
import operator
def max_subarray_nlgn(arr):
    """
    divide and conquer solution for the maximum sum subarray problem.
    let m=len(arr)/2. find the maximum sum subarray in the left half (array left of m),
    find the maximum sum subarray in the right half (array right of m), find the maximum sum subarray
    crossing the middle by fanning out to the left of m, and to the right of m just summing linearly

    :param arr: any array
    :return: (maximum sum subarray, maximum sum)
    """

    if len(arr) == 1:
        return arr,arr[0]

    # // for rounding in python3
    midpoint = len(arr)//2
    left_half_arr = arr[0:midpoint]
    right_half_arr = arr[midpoint:]
    max_subarr_left_arr,max_subarr_left_arr_tot = max_subarray_nlgn(left_half_arr)
    max_subarr_right_arr,max_subarr_left_arr_tot = max_subarray_nlgn(right_half_arr)

    crs_right_bound = crs_left_bound = None
    right_crs_max = left_crs_max = -np.inf
    tot = 0
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
    return max([(max_subarr_left_arr,max_subarr_left_arr_tot),(max_subarr_right_arr,max_subarr_left_arr_tot),(np.concatenate([left_half_arr[crs_left_bound:],right_half_arr[:crs_right_bound+1]]),max_cross)],key=operator.itemgetter(1))

if __name__ == '__main__':
    arr = np.random.randint(low=-100,high=100, size=10)
    test_mat = np.zeros((len(arr),len(arr)))
    for i in range(len(arr)):
        for j in range(i,len(arr)):
            test_mat[i,j] = np.sum(arr[i:j+1])
    print(test_mat)
    inds = np.unravel_index(test_mat.argmax(),test_mat.shape)
    print("whole arr:",arr, test_mat[inds])
    print((inds,arr[inds[0]:inds[1]+1]))

    print(max_subarray_nlgn(arr))


