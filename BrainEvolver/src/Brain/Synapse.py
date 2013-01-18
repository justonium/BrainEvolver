'''
Created on Dec 30, 2012

@author: Justin
'''

from numpy import *
from copy import deepcopy
from Divisible import Divisible
import Neuron
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
fireTransformSize = transformSize(dataSize)
evolveTransformSize = transformSize(dataSize + 2*Neuron.dataSize)
"used to access data only in finalize"
fireTransform = dataSize
evolveTransform = dataSize + fireTransformSize
fireTransformEnd = fireTransform + fireTransformSize
evolveTransformEnd = evolveTransform + evolveTransformSize

divisionDataSize = dataSize + fireTransformSize + evolveTransformSize
dataTransformSize = transformSize(divisionDataSize)

class Synapse(Divisible):
  
  def __init__(self, node, prev, nextNeuron):
    "structure"
    self.prev = prev
    self.next = nextNeuron
    
    "division data"
    self.node = node
    
    "dynamic behavior of main attributes"
    self.fireTransform = None
    self.evolveTransform = None
    
    "utilities"
    self.accessDict = { \
        'activation' : lambda : self.data[activation], \
        'weight' : lambda : self.data[weight], \
        'evolveRateScale' : lambda : self.data[evolveRateScale], \
        'evolveRate' : lambda : self.data[evolveRate:evolveRateEnd] \
        }
    self.writeDict = { \
        'activation' : super(Synapse, self).writeValue(activation), \
        'weight' : self.writeValue(weight), \
        'evolveRateScale' : self.writeValue(evolveRateScale), \
        'evolveRate' : self.writeVector(evolveRate, evolveRateSize) \
        }
  
  def fire(self):
    next.inBuffer += self.weight * self.activation
    self.data = applyTransform(self.data, self.fireTransform)
    self.updateRates()
    pass #schedule new evolve time
  
  def evolve(self, time):
    transformParam = concatenate(self.data, self.prev.data, self.next.data)
    self.data = applyTransform(transformParam, self.evolveTransform)
    self.updateRates()
    pass #schedule new evolve time
  
  def updateRates(self):
    self.evolveRate = self.evolveRateScale * \
        sigmoid(applyTransform(self.data, self.evolveRate))
  
  def divide(self, chemicals):
    "apply left and right transforms to the data of left and right"
    left = deepcopy(self)
    right = deepcopy(self)
    left.node = self.node.left
    right.node = self.node.right
    left.data = applyTransform(self.data, self.node.leftTransform)
    right.data = applyTransform(self.data, self.node.rightTransform)
  
  def finalize(self):
    self.fireTransform = \
        rollTransform(self.data[fireTransform:fireTransformEnd], dataSize)
    self.evolveTransform = \
        rollTransform(self.data[evolveTransform:evolveTransformEnd], dataSize)
    self.data = self.data[:dataSize]
    self.data = None




