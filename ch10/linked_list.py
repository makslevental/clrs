import random

class LLNode:
    def __init__(self,prev,next,val):
        self.val = val
        self.prev = prev
        self.next = next

    def __eq__(self, other):
        return self.val == other

    def __str__(self):
        return str(self.val)

class DoubleLinkedList:
    def __init__(self,ls):
        self.head = LLNode(None,None,ls[0])
        ptr = self.head
        for x in ls[1:]:
            ptr.next = LLNode(ptr,None,x)
            ptr = ptr.next

        ptr.next = self.head
        self.head.prev = ptr

    # this is no longer a regular function but a constructor of sorts for generator objects
    # running this function returns a generator that has a method call __next__ the is called
    # every time
    def __iter__(self):
        ptr = self.head
        yield ptr
        ptr = ptr.next
        while ptr != self.head:
            yield ptr
            ptr = ptr.next

    # this function should return a value
    # def __next__(self):

    def __contains__(self, item):
        for x in self:
            if x.val == item:
                return True
        return False

    def __delitem__(self, key):
        for x in self:
            if x == key:
                if x.prev and x.next:
                    x.prev.next = x.next
                    x.next.prev = x.prev
                    del x.val

    def insert(self,x):
        t = LLNode(self.head.prev,self.head,x)
        self.head.prev.next = t
        self.head.prev = t



def print_tri(n):
    s = ''
    j = 0
    k = 1
    for i in range(n):
        s += ','+str(i+1)
        j += 1
        if j == k:
            s += '\n'
            j = 0
            k += 1
    return s


if __name__ == '__main__':


    s = random.sample(range(10000), 10)
    dd = DoubleLinkedList([1])

    # del dd[5]
    # #
    # # for v in s:
    # #     print(v in dd)
    #
    # for d in dd:
    #     print(d)
    #
    # dd.insert(2)
    # dd.insert(3)
    # dd.insert(4)
    #
    # for d in dd:
    #     print(d)
    print(print_tri(10))
