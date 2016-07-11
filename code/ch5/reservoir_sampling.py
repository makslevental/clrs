"""
reservoir sampling routines

collect a k random sample online, such that each element seen has a probability of k/n of being in the sample
(where n is the number of elements seen).
"""

import numpy as np
import unittest
import queue

def algo_r(k: int,seq: list) -> list:
    res = seq[:k]
    for i,v in enumerate(seq[k:], start=k):
        # very important inclusive range
        j = np.random.randint(0,i+1)
        if j<k:
            res[j] = v
    return res


def res_rand_sort(k: int, seq: list) -> list:
    Q = queue.PriorityQueue(k)
    for v in seq[:k]:
        r = round(np.random.uniform(),10)
        Q.put((-r,v))
    for v in seq[k:]:
        r = round(np.random.uniform(),10)

        if -r > Q.queue[0][0]:
            Q.get()
            Q.put((-r,v))
    return [v for r,v in Q.queue]

def weighted_res(k: int, seq: list) -> list:
    """
    suppose the input seq is a list of tuples where second coordinate
    is weighting. how to sample such that probability of ending up
    in the reservoir is that weight? simple: r -> r^1/w, but also it should
    be a min priority queue
    :param k:
    :param seq:
    :return:
    """
    Q = queue.PriorityQueue(k)
    for v,w in seq[:k]:
        r = np.random.rand()**(1/w)
        Q.put((r,v))
    for v,w in seq[k:]:
        r = np.random.rand()**(1/w)

        if r > Q.queue[0][0]:
            Q.get()
            Q.put((r,v))
    return [v for r,v in Q.queue]

class ResTest(unittest.TestCase):
    numtests = 1000000
    seq = list(range(100))

    def util_uni(self,fn):
        testd = {i:0 for i in range(100)}
        for i in range(self.numtests):
            res = fn(10, self.seq)
            for r in res:
                testd[r] += 1

        its = np.array(list(testd.values()))/sum(testd.values())
        try:
            self.assertAlmostEqual(np.mean(its),0.1, places=2)
            self.assertAlmostEqual(np.std(its),0.001, places=2)
        except AssertionError as a:
            print(its)
            raise a

    def testUni(self):
        self.util_uni(algo_r)
        self.util_uni(res_rand_sort)

    def testWeight(self):
        weights = np.random.randint(1,1000,100)
        weights = weights/sum(weights)
        seq = list(range(100))

        testd = {i:0 for i in range(100)}
        for i in range(self.numtests):
            res = weighted_res(10,list(zip(seq,weights)))
            for r in res:
                testd[r] += 1

        for k,v in testd.items():
            try:
                self.assertAlmostEqual(v/sum(testd.values()),weights[k],places=3)
            except AssertionError as a:
                print(k,v)
                raise a

if __name__ == '__main__':
    unittest.main()

