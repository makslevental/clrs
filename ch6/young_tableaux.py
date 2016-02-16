import numpy as np
import math


class YoungTableaux:
    def __init__(self,ls=None):
        if ls is None:
            self.ls = []
        else:
            self.ls = ls
            self.mat = np.full((math.ceil(math.sqrt(2*len(ls))),math.ceil(math.sqrt(2*len(ls)))),fill_value=np.inf)
            #self.mat = np.full((math.ceil(math.sqrt(len(ls))),math.ceil(math.sqrt(len(ls)))),fill_value=np.inf)
            for x in ls:
                self.push(x)

    def _check_grow(self):
        _, count = np.unique(self.mat, return_counts=True)
        if count[-1] < self.mat.size//2:
            pad_width = math.ceil(math.sqrt(self.mat.size)*(math.sqrt(2)-1))
            self.mat = np.lib.pad(self.mat,((0,pad_width),(0,pad_width)),'constant',constant_values=np.inf)

    def _perc_up(self,i,j):

        while True:
            if i == -self.mat.shape[0] and j > -self.mat.shape[1] and self.mat[i,j] < self.mat[i,j-1]:
                self.mat[i,j], self.mat[i,j-1] = self.mat[i,j-1], self.mat[i,j]
                j += -1
            elif j == -self.mat.shape[1] and i > -self.mat.shape[0] and self.mat[i,j] < self.mat[i-1,j]:
                self.mat[i,j], self.mat[i-1,j] = self.mat[i-1,j], self.mat[i,j]
                i += -1
            elif (i > -self.mat.shape[0] and j > -self.mat.shape[1]) and\
                    (self.mat[i,j] < self.mat[i-1,j] or self.mat[i,j] < self.mat[i,j-1]):
                #switch with the largest one
                e = largest = self.mat[i,j]
                largest_inds = i,j
                if e < self.mat[i-1,j]:
                    largest = self.mat[i-1,j]
                    largest_inds = i-1,j

                if largest < self.mat[i,j-1]:
                    largest = self.mat[i,j-1]
                    largest_inds = i,j-1

                self.mat[i,j], self.mat[largest_inds] = self.mat[largest_inds], self.mat[i,j]
                i,j = largest_inds
            else:
                break

    def _perc_down(self,i,j):
        try:
            while self.mat[i,j] > self.mat[i+1,j] or self.mat[i,j] > self.mat[i,j+1]:
                    if self.mat[i,j] > self.mat[i+1,j]:
                        self.mat[i,j], self.mat[i+1,j] = self.mat[i+1,j], self.mat[i,j]
                        i = i+1
                    else:
                        self.mat[i,j], self.mat[i,j+1] = self.mat[i,j+1], self.mat[i,j]
                        j = j+1
        except IndexError:
            pass

    def push(self,x):
            self._check_grow()
            self.mat[-1,-1] = x
            self._perc_up(-1,-1)

    def extract_min(self):
        m = self.mat[0,0]
        self.mat[0,0] = self.mat[-1,-1]
        self._perc_down(0,0)
        return m

    def check_mem(self,x):
        # start at the top right. everything to the left is less
        # and every below is greater. if greater than then go left, if less than then go down
        i,j = 0,-1

        k = self.mat[i,j]
        try:
            while k != x:
                if k > x:
                    i += -1
                else:
                    j += 1
        except IndexError:
            return (-1,-1),False
        else:
            return (i,j),True


# 6.5-9 use minheap to give an o(nlgk) algo for producing a sorted array from k sorted arrays
# use the minheap to do k way merging i.e. take the first element of every array, make a minheap out of them.
# that costs o(k). then pop into another array (they'll come out sorted). that costs O(klgk). total cost O(k) +
# O(klgk) = O(klgk) do this for n/k times and you get O(n/k k lgk) = O(n lgk)

# well that's wrong because why would the final array be sorted?
# correct solution: take the first element of each array and construct a min heap. take the min and
# put it into a new array. then take an element from the same array that that min came from and push it to
# min heap. you do this so the "top" (i.e. the min) of each individual array is always represented in the
# in the heap (so that all of the minima at any given moment of the individual arrays are in direct competition)

# 6-3 young tableaus
# 6.3c give an O(m+n) algo for extracting min from an m x n young tableau
# well Y[1,1] is clearly the min. how to extract it? the hint is to think about Max-heapify (which percolates down)
# so maybe extract min then replace by bottom right? and flip entries until it's back in the correct position?
# so put the entry in the top left and then replace it with the smallest of the neighboring entries and then repeat?
# the entry can travel at max m+n squares.
#
# 6.3d insert similar to a min heap: but at the bottom right and then percolate up, swapping with larger of the neighbors
# and repeat. this works because flipping with the larger preserves the invariant with the respect to the smaller one
# and the new entry with respect to the flipped one. stop when the new entry is larger than both neighbors

# 6.3e insert the n^2 numbers then extract min. insertion costs O(n) time and extract min costs O(n) time, so
# n x O(n) x O(n).

# 6.3f
# how not to miss it? start from the top right. that way you know everything below you is greater and everything
# to the left is smaller. if you're greater than then go left, if you're smaller than then go down.
