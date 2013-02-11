'''
Created on Feb 10, 2013

@author: Justin
'''

from Body.ArrayInterface import ArrayInterface
from Brain import *
import random

dataSize = 5
codeSize = 1

lifespan = 60.0
spawnRate = 0.1



class Bot(object):
  
  def __init__(self):
    moves = [('left', 1), ('right', 1), ('up', 1), ('down', 1)]
    self.outputs = ArrayInterface(moves + [('dataOut', dataSize), ('code', codeSize)])
    
    self.inputs = ArrayInterface([('dataIn', dataSize), ('birth', 1)])
    
    self.brain = createEmpty(self.inputs.size, self.outputs.size)
    
    self.age = 0.0
    self.lifespan = random.expovariate(1/lifespan)
    self.spawnTime = random.expovariate(spawnRate)
  
  def spawn(self):
    child = Bot()
    child.brain = self.brain.spawn()
    self.spawnTime = random.expovariate(spawnRate)
    return child
  
  def elapseTime(self, time, correct):
    self.age += time
    if (self.age > self.lifespan):
      return False
    
    if (correct):
      self.spawnTime -= time
    
    self.brain.elapseTime(time, self.inputs.data)
    self.outputs.data = self.brain.outputs
    return True












