import numpy as np
import unittest
from ch6.young_tableaux import YoungTableaux
import itertools


class TestYoung(unittest.TestCase):
    def testBuild(self):
        for i in range(1,100):
            ls = np.random.randint(1,100,i).astype(np.float64)
            y = YoungTableaux(ls)

            try:
                for ind in itertools.product(range(1,y.mat.shape[0]),range(1,y.mat.shape[1])):
                    x = y.mat[ind]
                    self.assertLessEqual(y.mat[ind[0],ind[1]-1],x)
                    self.assertLessEqual(y.mat[ind[0]-1,ind[1]],x)
            except AssertionError:
                print(ind,y.mat)
                raise