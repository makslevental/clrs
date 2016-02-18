import unittest
from ch8 import counting_sort as ct
from ch7 import quicksort as qk
import numpy as np


class SortTest(unittest.TestCase):
    iters = 1000

    def FtestCount(self, sortfun):
        for i in range(self.iters):
            t = list(np.random.randint(1,10000,100))
            try:
                s = sortfun(t)

            except AssertionError:
                print(t,s)
                raise

    def testCountBackward(self):
        self.FtestCount(ct.counting_sort_backwards)

    def testCountForward(self):
        self.FtestCount(ct.counting_sort_forwards)

    def testQuickEasy(self):
        self.FtestCount(qk.quick_sort_easy)

    def testQuickHard(self):
        self.FtestCount(qk.quick_sort_hard)

    def testQuickHard(self):
        self.FtestCount(ct.counting_sort_backwards_neg)
