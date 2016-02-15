import numpy as np
import math
class YoungTableaux:
    def __init__(self,ls=None):
        if ls is None:
            self.ls = []
        else:
            self.ls = ls
            self.mat = np.full(math.ceil(math.sqrt(2*len(ls))),2*math.ceil(math.sqrt(2*len(ls))),np.inf)
            for x in ls:
                self.push(x)

    def _check_grow(self):
        _, count = np.unique(self.mat, return_counts=True)
        if count[-1] < self.mat.size//2:
            pad_width = math.sqrt(self.mat.size)*(math.sqrt(2)-1)
            np.lib.pad(self.mat,((0,pad_width),(0,pad_width)),'constant',constant_values=np.inf)

    def _perc_up(self,i,j):
        while self.mat[i,j] < self.mat[i-1,j] or self.mat[i,j] < self.mat[i,j-1]:
                if self.mat[i,j] < self.mat[i-1,j]:
                    self.mat[i,j], self.mat[i-1,j] = self.mat[i-1,j], self.mat[i,j]
                    i = i-1
                else:
                    self.mat[i,j], self.mat[i,j-1] = self.mat[i,j-1], self.mat[i,j]
                    j = j-1


    def _perc_down(self,i,j):
        while self.mat[i,j] > self.mat[i+1,j] or self.mat[i,j] > self.mat[i,j+1]:
                if self.mat[i,j] > self.mat[i+1,j]:
                    self.mat[i,j], self.mat[i+1,j] = self.mat[i+1,j], self.mat[i,j]
                    i = i+1
                else:
                    self.mat[i,j], self.mat[i,j+1] = self.mat[i,j+1], self.mat[i,j]
                    j = j+1

    def push(self,x):
            self._check_grow()
            self.mat[-1,-1] = x
            self._perc_up(-1,-1)

    def extract_min(self):
        m = self.mat[0,0]
        self.mat[0,0] = self.mat[-1,-1]
        self._perc_down(0,0)

    def check_mem(self,x):
        pass
