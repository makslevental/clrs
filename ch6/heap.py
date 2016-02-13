"""
heap class and methods
"""
from collections import deque
import operator
import numpy as np
import unittest


class Infix:
    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __or__(self, other):
        return self.function(other)

    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __rshift__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self.function(value1, value2)


class Heap:

    def __init__(self, op, ls):
        self.op = op
        self.arr = deque(ls)
        self.__build_heap()

    def __getitem__(self, ind):
        return self.arr[ind]

    def __setitem__(self, key, value):
        self.arr[key] = value

    def __delitem__(self, key):
        del self.arr[key]

    def __repr__(self):
        return str(self.arr)[5:]

    def __iter__(self):
        return iter(self.arr)


    def __len__(self):
        return len(self.arr)

    @staticmethod
    def _parent(i):
        if i == 0: return 0
        else: return (i-1)//2

    @staticmethod
    def _left(i):
        return (2*i)+1

    @staticmethod
    def _right(i):
        return (2*i+1)+1

    def _perc_down(self, i):
        ind = i
        while ind+1 < len(self.arr):
            l = self._left(ind)
            r = self._right(ind)
            try:
                if self.arr[l] <<self.op>> self.arr[ind]: largest = l
                else: largest = ind
            except IndexError:
                largest = ind

            try:
                if self.arr[r] <<self.op>> self.arr[largest]: largest = r
            except IndexError:
                pass

            if largest != ind:
                self.arr[largest],self.arr[ind] = self.arr[ind],self.arr[largest]
                ind = largest
            else:
                break

    def _perc_up(self,i):
        while i > 0 and self[i] <<self.op>> self[self._parent(i)]:
            self[i], self[self._parent(i)] = self[self._parent(i)], self[i]
            i = self._parent(i)
    """
    O(n) time versus O(nlgn) for inserting and using heapify. why?
    one run of max_heapify costs O(h)=O(lgn) time but you don't need
    to run it on the leaves because they already satisfy the max heap property AND
    the height of most nodes is very small (for example only the root node has height h).
    so for how many entries do we do this and how high are there?
    well there are n/2^h entries for each height h, so sum(n/2^h)*O(h) = O(n sum(h/2^h)) = O(2*n)
    """
    def __build_heap(self):
        for i in range(len(self.arr)//2,-1,-1):
            self._perc_down(i)

    def __incr_key(self,i,key):
        if self[i] <<self.op>> key:
            raise Exception('key is '+ 'less than ' if self.op == operator.gt else 'greater than ' + 'current key')
        self[i] = key
        self._perc_up(i)



    def empty(self):
        return len(self) < 1

    def push(self,x):
        # self.arr.appendleft(x)
        # this is wrong. the only reason this works (efficiently) is because of dequeue
        # otherwise what happens when you insert in sorted order? are you creating new
        # roots?
        #self._perc_down(0)
        self.arr.append(x)
        self._perc_up(len(self)-1)

    def top(self):
        return self[0]

    def pop(self):
        if self.empty(): raise IndexError
        t = self.top()
        self.delete(0)
        return t

    def delete(self,i):
        if self.empty(): raise IndexError
        self[i] = self[len(self)-1]
        del self[len(self)-1]
        # if you remove the root element of the heap
        # each of children of the root still satisfy
        # the heap property on their own. so we need to
        # merge the two trees without introducing another
        # element: substituting the last element breaks
        # the heap property of at the root so we need to restore it
        self._perc_down(i)


class MaxHeap(Heap):

    def __init__(self,ls):
        Heap.__init__(self, Infix(operator.gt),ls)


class MinHeap(Heap):
    def __init__(self,ls):
        Heap.__init__(self, Infix(operator.lt),ls)


class PriorityQueue(MinHeap):
    pass

class TestHeap(unittest.TestCase):
    def testBuildHeap(self):
        try:
            for j in range(1,100):
                test_arr = np.random.randint(0,j,j)
                h = MinHeap(test_arr)
                for i,v in reversed(list(enumerate(h))):
                    self.assertLessEqual(h[Heap._parent(i)],v)

                s_test_arr = sorted(test_arr)
                while len(h) > 0:
                    s_test_arr.pop() == h.pop()

                test_arr = np.random.randint(0,j,j)
                h = MaxHeap(test_arr)
                for i,v in reversed(list(enumerate(h))):
                    self.assertGreaterEqual(h[Heap._parent(i)],v)

                s_test_arr = list(reversed(sorted(test_arr)))
                while len(h) > 0:
                    s_test_arr.pop() == h.pop()
        except AssertionError as a:
            print(h,Heap._parent(i),i,sep='\n')

if __name__ == '__main__':
    unittest.main()



# 6.1-1 what are the min and max number of elements in a heap of height h?
# a regular heap (not min or max) is same as complete binary tree
# h=0:1, h=1:1+1, h=2:3+1,h=3:7+1. so for h=1:[2,3],h=2:[4,7]. so [2^h,2^{h+1}-1]

# 6.1-2 show that an n-element heap has height floor(lgn)
# 3 elements = h = 2 log2(3). since an h height heap stores between 2^h and 2^{h+1}-1
# hence 2^h =n -> h = log2(n)

# 6.1-3 for a maxheap A[parent(i)] >= A[i]. since A[root] >= A[i] in its subtree
# the root is max

# 6.1-4 the smallest element is at a node, otherwise it would violate A[parent(i)] >= A[i]

# 6.1-5 yes since the children of any i are greater than, hence satisfying the min heap property

# 6.1-6  skip

# 6.1-7 prove in the array representation of a heap the leaves are in the second half of the array
# well a complete binary tree holds half of its element in the bottom layer

# 6.5-7 fifo using a priority queue: duh key on insertion time
# 6.5-7 stack using a priority queue: key on negative insertion time

# 6.5-9 use minheap to give an o(nlgk) algo for producing a sorted array from k sorted arrays
# use the minheap to do k way merging i.e. take the first element of every array, make a minheap out of them.
# that costs o(k). then pop into another array (they'll come out sorted). that costs O(klgk). total cost O(k) +
# O(klgk) = O(klgk) do this for n/k times and you get O(n/k k lgk) = O(n lgk)

# well that's wrong because why would the final array be sorted?
# correct solution: take the first element of each array and construct a min heap. take the min and
# put it into a new array. then take an element from the same array that that min came from and push it to
# min heap. you do this so the "top" (i.e. the min) of each individual array is always represented in the
# in the heap (so that all of the minima at any given moment of the individual arrays are in direct competition)
