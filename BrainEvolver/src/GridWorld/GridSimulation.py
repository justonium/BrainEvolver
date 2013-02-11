'''
Created on Feb 10, 2013

@author: Justin
'''

import Brain
from Brain import Neuron
from Brain import Synapse
from Brain import *
from Bot import *
from Grid import *
import numpy as np
import random

gridWidth = 10
gridHeight = 10
numBots = 50
timeStepSize = 0.1
codeRefreshRate = 0.1
reportFrequency = 1

stepsPerReport = int(np.ceil(reportFrequency/timeStepSize))



class GridSimulation(object):
  
  "inititialize the world"
  def __init__(self):
    self.grid = Grid(gridWidth, gridHeight)
    for i in range(numBots):
      self.age = 0.0
      bot = Bot()
      x = random.randint(0, gridWidth-1)
      y = random.randint(0, gridWidth-1)
      self.grid.getNode(x, y).bots.add(bot)
      self.createCode()
      self.stepCount = 0
  
  def createCode(self):
    self.code = np.random.random_integers(0, 1, codeSize)
    self.refreshAge = self.age + random.expovariate(codeRefreshRate)
    
  "run the simulation"
  def elapseTime(self, time):
    goalAge = self.age + time
    while (self.age < goalAge):
      
      "report"
      if (self.stepCount <= 0):
        self.stepCount += stepsPerReport
        numBots = 0
        for x in range(self.grid.width):
          for y in range(self.grid.height):
            numBots += len(self.grid.getNode(x, y).bots)
        print 'Time:', self.age, 'Number of Bots:', numBots
      self.stepCount -= 1
      
      self.age += timeStepSize
      if (self.age > self.refreshAge):
        self.createCode()
      
      "run the bots"
      for x in range(self.grid.width):
        for y in range(self.grid.height):
          node = self.grid.getNode(x, y)
          for bot in node.bots:
            "push their outputs to the node"
            node.data += bot.outputs.dataOut
          for bot in node.bots.copy():
            "listen to accumulated outputs"
            bot.inputs.dataIn = node.data
            node.clearData()
            
            "determine move"
            left = bot.outputs.left > random.random()
            right = bot.outputs.right > random.random()
            up = bot.outputs.up > random.random()
            down = bot.outputs.down > random.random
            if (left and right):
              left = False
              right = False
            if (up and down):
              up = False
              down = False
            
            "determine new coordinates"
            newx = x
            newy = y
            if (left):
              newx -= 1
            if (right):
              newx += 1
            if (up):
              newy += 1
            if (down):
              newy -= 1
            
            "make move"
            if ((x, y) != (newx, newy)):
              node.bots.remove(bot)
              self.grid.getNode(newx, newy).bots.add(bot)
            
            "reproduce"
            if (bot.spawnTime <= 0.0):
              node.bots.add(bot.spawn())
            
            "elapse bot time and remove dead bots"
            guess = bot.outputs.code
            guess = np.maximum(guess, 0)
            guess = np.minimum(guess, 1)
            correct = reduce(lambda x, y : x * y, np.abs(guess - self.code)) < random.random()
            alive = bot.elapseTime(timeStepSize, correct)
            if (not alive):
              node.bots.remove(bot)


















