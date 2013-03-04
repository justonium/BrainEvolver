'''
Created on Feb 10, 2013

@author: Justin
'''

try:
  from numpypy import *
except:
  from numpy import *
from Bot import *



class Grid(object):
  
  def __init__(self, gridWidth, gridHeight):
    self.array = [[Node() for i in range(gridHeight)] for i in range(gridWidth)]
    self.width = gridWidth
    self.height = gridHeight
  
  def getNode(self, x, y):
    x = x % self.width
    y = y % self.height
    return self.array[x][y]
  
  def numBots(self):
    numBots = 0
    for x in range(self.width):
      for y in range(self.height):
        numBots += len(self.getNode(x, y).bots)
    return numBots
  
  def numCorrect(self):
    numCorrect = 0
    for x in range(self.width):
      for y in range(self.height):
        for bot in self.getNode(x, y).bots:
          numCorrect += 1 if bot.inputs.correct > 0.5 else 0
    return numCorrect

class Node(object):
  
  def __init__(self):
    self.bots = set()
    self.data = zeros(dataSize)
  
  def clearData(self):
    self.data = zeros(dataSize)
  
  def add(self, bot):
    self.bots.add(bot)
    bot.node = self
  
  def remove(self, bot):
    self.bots.remove(bot)
    bot.node = None