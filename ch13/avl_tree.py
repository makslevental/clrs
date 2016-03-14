from ch12.bst import TreeNode, BinarySearchTree

class AVLNode(TreeNode):
    def __init__(self, val=None, prnt=None, lchild=None, rchild=None, height=0):
        super().__init__(val, prnt, lchild, rchild)
        self.height = height


class AVLTree(BinarySearchTree):
    pass