'''
Created on Dec 30, 2012

@author: Justin
'''

from numpy import *
from heapq import *
from copy import deepcopy
from Cell import Cell
import Neurons
from Tools import *

"main attributes"
activation = 0
weight = 1
evolveRateScale = 2

"paramSize < dataSize < divisionDataSize"
numAttributes = 3
numChemicals = 5
paramSize = numAttributes + numChemicals

evolveRateSize = reduceSize(paramSize)
"also used to access data"
evolveRate = paramSize
evolveRateEnd = evolveRate + evolveRateSize

dataSize = paramSize + evolveRateSize
fireTransformWidth = dataSize + 2*Neurons.dataSize
evolveTransformWidth = dataSize + 2*Neurons.dataSize
fireTransformSize = transformSize(fireTransformWidth)
evolveTransformSize = transformSize(fireTransformWidth)
"used to access data only in finalize"
fireTransform = dataSize
evolveTransform = dataSize + fireTransformSize
fireTransformEnd = fireTransform + fireTransformSize
evolveTransformEnd = evolveTransform + evolveTransformSize

divisionDataSize = dataSize + fireTransformSize + evolveTransformSize
divisionTransformWidth = divisionDataSize + 2*Neurons.divisionDataSize



class Synapse(Cell):
  
  def __init__(self, node, source, sink, data):
    "structure"
    self.brain = None
    self.source = source
    self.sink = sink
    
    "division data"
    self.node = node
    self.data = data
    
    self.evolveRate = None
    
    "dynamic behavior of main attributes"
    self.fireTransform = None
    self.evolveTransform = None
    
    "utilities"
    self.nextEvent = None
    self.accessDict = { \
        'activation' : lambda : self.data[activation], \
        'weight' : lambda : self.data[weight], \
        'evolveRateScale' : lambda : self.data[evolveRateScale], \
        'params' : lambda : self.data[:paramSize], \
        'evolveRateFun' : lambda : self.data[evolveRate:evolveRateEnd] \
        }
    self.writeDict = { \
        'activation' : super(Synapse, self).writeValue(activation), \
        'weight' : self.writeValue(weight), \
        'evolveRateScale' : self.writeValue(evolveRateScale), \
        'params' : lambda : self.writeValue(0, paramSize), \
        'evolveRateFun' : self.writeVector(evolveRate, evolveRateSize) \
        }
  
  def fire(self, source):
    sink = self.sink if source == self.source else self.source
    sink.inBuffer += self.weight * self.activation
    transformParam = concatenate(self.data, source.data, sink.data)
    self.data += applyTransform(transformParam, self.fireTransform)
    self.nextEvent.active = False
    self.schedule()
  
  def evolve(self, time):
    transformParam = concatenate(self.data, self.source.data, self.sink.data)
    self.data += applyTransform(transformParam, self.evolveTransform)
    self.schedule()
  
  "enqueues new events"
  def schedule(self):
    self.updateRates()
    delay = sampleDelay(self.evolveRate)
    action = self.evolve
    if (delay < inf):
      self.pushEvent(action, self.source.brain.currentTime + delay)
  
  def updateRates(self):
    self.evolveRate = self.evolveRateScale * \
        sigmoid(applyTransform(self.params, self.evolveRateFun))
  
  def divide(self, chemicals):
    "apply left and right transforms to the data of left and right"
    left = deepcopy(self)
    right = deepcopy(self)
    left.node = self.node.left
    right.node = self.node.right
    "make transforms use source and sink!"
    leftTransformParam = concatenate(self.data, self.source.data, self.sink.data)
    rightTransformParam = concatenate(self.data, self.source.data, self.sink.data)
    left.data = self.data + applyTransform(leftTransformParam, self.node.leftTransform)
    right.data = self.data + applyTransform(rightTransformParam, self.node.rightTransform)
  
  def finalize(self):
    if (self.node.symmetric):
      self.sink.inSynapses.remove(self)
      self.sink.outSynapses.add(self)
    self.fireTransform = \
        rollTransform(self.data[fireTransform:fireTransformEnd], fireTransformWidth)
    self.evolveTransform = \
        rollTransform(self.data[evolveTransform:evolveTransformEnd], evolveTransformWidth)
    self.data = self.data[:dataSize]
    self.node = None
  
  def spawn(self):
    pass











