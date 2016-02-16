import numpy as np
import unittest
from ch6.young_tableaux import YoungTableaux
import itertools


class TestYoung(unittest.TestCase):
    iterations = 100
    def FtestInvariant(self,y):
        try:
            for ind in itertools.product(range(1,y.mat.shape[0]),range(1,y.mat.shape[1])):
                x = y.mat[ind]
                self.assertLessEqual(y.mat[ind[0],ind[1]-1],x)
                self.assertLessEqual(y.mat[ind[0]-1,ind[1]],x)
        except AssertionError:
            print(ind,y.mat)
            raise

    def testBuild(self):
        for i in range(1,self.iterations):
            ls = np.random.randint(1,100,i).astype(np.float64)
            y = YoungTableaux(ls)
            self.FtestInvariant(y)

    def testExtract(self):
        for i in range(1,self.iterations):
            ls = np.random.randint(1,100,i).astype(np.float64)
            sorted_ls = sorted(ls)

            y = YoungTableaux(ls)

            try:
                for e in sorted_ls:
                    self.assertEqual(e,y.extract_min())
                    self.FtestInvariant(y)
            except AssertionError:
                print(e,sorted_ls,y.mat)
                raise

    def testSearch(self):
        for i in range(1,self.iterations):
            ls = np.random.rand(1,i)[0]
            y = YoungTableaux(ls)

            for ind in itertools.product(range(-1,-y.mat.shape[0]-1,-1),range(-1,-y.mat.shape[1]-1,-1)):
                if y.mat[ind] == np.inf: continue
                else: self.assertEqual((ind,True), y.search(y.mat[ind]))

            for x in ls-1:
                self.assertFalse(y.search(x)[1])