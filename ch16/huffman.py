from ch10.treenode import TreeNode
from queue import PriorityQueue

class HuffTree():
    def __init__(self):
        self.root = TreeNode()

    def encode(self,ls):
        q = PriorityQueue(ls)
