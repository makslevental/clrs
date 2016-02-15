import numpy as np
import unittest
from ch6.heap import BaseHeap, MinHeap, MaxHeap


class TestHeap(unittest.TestCase):

    def FtestBuildHeap(self,heap):
        try:
            for i,v in enumerate(heap):
                self.assertTrue(heap[BaseHeap._parent(i)] <<heap.op>> v)
        except AssertionError as a:
            print(heap, BaseHeap._parent(i), i, sep='\n')
            raise a

    def testBuildMinHeap(self):
        for j in range(2,100):
            test_arr = np.random.randint(0,j,j)
            h = MinHeap(test_arr)
            self.FtestBuildHeap(h)

    def testBuildMaxHeap(self):
        for j in range(2,100):
            test_arr = np.random.randint(0,j,j)
            h = MaxHeap(test_arr)
            self.FtestBuildHeap(h)

    def FtestSortedHeap(self,heap,arr):
        try:
            while len(heap) > 0:
                hh = heap.extract_top()
                ss = arr.pop()
                self.assertEqual(ss,hh)
        except AssertionError as a:
            print(heap, arr, sep='\n')
            raise a

    def testSortedMinHeap(self):
        for j in range(2,100):
            test_arr = np.random.randint(0,j,j)
            h = MinHeap(test_arr)
            self.FtestSortedHeap(h,list(reversed(sorted(test_arr))))

    def testSortedMaxHeap(self):
        for j in range(2,100):
            test_arr = np.random.randint(0,j,j)
            h = MaxHeap(test_arr)
            self.FtestSortedHeap(h,list(sorted(test_arr)))

    def testPushMinHeap(self):

        for j in range(2,100):
            test_arr = np.random.randint(0,j,j)
            h = MinHeap()
            for t in test_arr:
                h.push(t)

            self.FtestBuildHeap(h)

    def testPushMaxHeap(self):

        for j in range(2,100):
            test_arr = np.random.randint(0,j,j)
            h = MaxHeap()
            for t in test_arr:
                h.push(t)

            self.FtestBuildHeap(h)

# if __name__ == '__main__':
#     unittest.main()
#     # m = MaxHeap([4,5,2,1,6,9,0,1])
#     # while not m.empty():
#     #     print(m.extract_top())
