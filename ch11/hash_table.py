import math

class HashTable:


    def __init__(self):
        self.arr = 128*[[]]
        self.load = 0

    def _hashfn(self,k):
        a = 2654435769/2**32
        return math.floor(len(self.arr)*(k*a-math.floor(k*a)))

    def _grow(self):
        self.arr.extend((len(self.arr)*[None]))

    def _shrink(self):
        self.arr = self.arr[:len(self.arr)//2]

    def insert(self,x):
        if self.load/len(self.arr) > .5:
            self._grow()

        self.arr[self.hashfn(x)].append(x)
        self.load += 1

    def delete(self,x):
        tarr = self.hashfn(x)
        self.arr[self.hashfn(x)] = filter(lambda y: y != x,tarr)
        self.load -= 1
        if self.load/len(self.arr) <= .5:
            self._shrink()

    def check(self,x):
        return self.arr[self.hashfn(x)] == x



# 11.1-3 use chaining

# 11.1-2 use the bitmap to indicate membership

# 11.1-4 use the stack to store the actual values. in the huge array store the index into the "stack"
# check to make sure key1->index->(key2,value) key1==key2. insertions get the top of the stack
# deletions involve swapping in the stack and the huge array and assigning nulls and popping the stack

# 11.2-5 pigeonhole

# 11.2-6 keyword being randomly (not just any). pick a random bucket with k elements then pick an index i from 1..L.
# reject i > k (essentially rejection sampling the array, i.e. how to randomly pick an element from 1..k if you can generate
# random numbers from 1 to L. since the load is n/m the expected number of elements k = n/m and so probability of i <= k =
# (n/m)/L  and hence expected number of times before success is 1/[(n/m)/L] = L*m/n (picking hte initial bucket doesn't affect
# do "cost" anything. hence combined with time L to traverse we get L+L*m/n = L(1+1/a)