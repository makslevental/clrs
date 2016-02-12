"""
heap class and methods
"""
from collections import deque

class Heap:

    arr = deque()

    def __parent(self,i):
        return (i-1)//2

    def __left(self,i):
        return (2*i)+1

    def __right(self,i):
        return (2*i+1)+1

    def _max_heapify(self, i):
        ind = i
        while ind+1 < len(self.arr):
            l = self.__left(ind)
            r = self.__right(ind)
            try:
                if self.arr[l] > self.arr[ind]: largest = l
                else: largest = ind
            except IndexError:
                largest = ind

            try:
                if self.arr[r] > self.arr[largest]: largest = r
            except IndexError:
                pass

            if largest != ind:
                self.arr[largest],self.arr[ind] = self.arr[ind],self.arr[largest]
                ind = largest
            else:
                break

    def push(self,x):
        self.arr.appendleft(x)
        self._max_heapify(0)


if __name__ == '__main__':
    h = Heap()
    h.push(2)
    h.push(1)
    h.push(3)
    h.push(-1)
    print(h.arr)



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