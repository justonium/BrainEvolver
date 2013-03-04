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
try:
  from numpypy import *
except:
  from numpy import *
  import numpy.random as nprandom
import random
import math
import pickle

gridWidth = 10
gridHeight = 10
numBots = 1
maxBots = 10
timeStepSize = 0.5
codeRefreshRate = 0.2
reportFrequency = 1

stepsPerReport = int(ceil(reportFrequency/timeStepSize))



class GridSimulation(object):
  
  "inititialize the world"
  def __init__(self):
    self.grid = Grid(gridWidth, gridHeight)
    for i in range(numBots):
      self.age = 0.0
      bot = Bot()
      x = random.randint(0, gridWidth-1)
      y = random.randint(0, gridWidth-1)
      self.grid.getNode(x, y).add(bot)
      self.createCode()
      self.stepCount = 0
  
  def createCode(self):
    #self.code = nprandom.random_integers(0, 1, codeSize)
    self.code = zeros(codeSize)
    for i in range(codeSize):
      self.code[i] = random.randint(0, 1)
    self.refreshAge = self.age + random.expovariate(codeRefreshRate)
    
  "run the simulation"
  def elapseTime(self, time):
    goalAge = self.age + time
    while (self.age < goalAge):
      
      "report"
      if (self.stepCount <= 0):
        self.stepCount += stepsPerReport
        numBots = self.grid.numBots()
        numCorrect = self.grid.numCorrect()
        print 'Time:', self.age, 'Number of Bots:', numBots, 'Code:', self.code, \
        'Percent correct:', float(numCorrect)/numBots
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
            down = bot.outputs.down > random.random()
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
            
            node2 = node
            "make move"
            if ((x, y) != (newx, newy)):
              node.remove(bot)
              node2 = self.grid.getNode(newx, newy)
              node2.add(bot)
            
            "reproduce"
            if (bot.spawnTime <= 0.0):
              node2.add(bot.spawn())
            
            "elapse bot time and remove dead bots"
            guess = bot.outputs.code
            guess = maximum(guess, 0)
            guess = minimum(guess, 1)
            correct = reduce(lambda x, y : x * y, abs(guess - self.code)) < random.random()
            #bot.inputs.correct = 1 if correct else 0
            #debug
            bot.inputs.correct = self.code[0]
            print correct
            
            alive = bot.elapseTime(timeStepSize)
            if (not alive):
              node2.remove(bot)
      
      "kill extra bots"
      bots = []
      for x in range(self.grid.width):
        for y in range(self.grid.height):
          node = self.grid.getNode(x, y)
          bots.extend(node.bots)
      random.shuffle(bots)
      for i in range(maxBots, len(bots)):
        bots[i].node.remove(bots[i])
















