'''
Created on Feb 10, 2013

@author: Justin
'''

from numpy import *
from Bot import *



class Grid(object):
  
  def __init__(self, gridWidth, gridHeight):
    self.array = [[Node() for i in range(gridHeight)] for i in range(gridWidth)]
    self.width = gridWidth
    self.height = gridHeight
  
  def getNode(self, x, y):
    x = mod(x, self.width)
    y = mod(y, self.height)
    return self.array[x][y]

class Node(object):
  
  def __init__(self):
    self.bots = set()
    self.data = zeros(dataSize)
  
  def clearData(self):
    self.data = zeros(dataSize)