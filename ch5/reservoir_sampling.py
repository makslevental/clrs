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
    res = seq[:k]
    Q = queue.PriorityQueue(k)
    for v in seq[:k]:
        r = round(np.random.uniform(),10)
        Q.put((-r,v))
    for v in seq[k:]:
        r = round(np.random.uniform(),10)

        if -r > Q.queue[0][0]:
            t = Q.get()
            Q.put((-r,v))
    return [v for r,v in Q.queue]


class ResTest(unittest.TestCase):
    seq = list(range(100))

    def testUni(self):
        testd = {i:0 for i in range(100)}
        for i in range(100000):
            res = res_rand_sort(10, self.seq)
            for r in res:
                testd[r] += 1

        its = np.array(list(testd.values()))/100000
        try:
            self.assertAlmostEqual(np.mean(its),0.1, places=2)
            self.assertAlmostEqual(np.std(its),0.001, places=2)
        except AssertionError as a:
            print(its)
            raise a

if __name__ == '__main__':
    unittest.main()

        # print(np.mean(its),np.std(its))
    # plt.bar(range(len(its)),its,1/1.5)
    # plt.show()
    # mu, sigma = 100, 15
    # x = mu + sigma*np.random.randn(10000)
    #
    # # the histogram of the data
    # n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
    #
    # # add a 'best fit' line
    # y = mlab.normpdf( bins, mu, sigma)
    # l = plt.plot(bins, y, 'r--', linewidth=1)
    #
    # plt.xlabel('Smarts')
    # plt.ylabel('Probability')
    # plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    # plt.axis([40, 160, 0, 0.03])
    # plt.grid(True)
    #
    # plt.show()