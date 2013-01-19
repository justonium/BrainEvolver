'''
Created on Dec 30, 2012

@author: Justin
'''
from numpy import *
from heapq import *
from Cell import Cell
import Synapses
from Tools import *
from copy import deepcopy

'''main attributes'''
sensitivity = 0
bias = 1
input = 2
fireRateScale = 3
evolveRateScale = 4

"paramSize < dataSize < divisionDataSize"
numAttributes = 5
numChemicals = 5
params = 0
paramSize = numAttributes + numChemicals

fireRateSize = reduceSize(paramSize)
evolveRateSize = reduceSize(paramSize)
"also used to access data"
fireRate = paramSize
evolveRate = paramSize + fireRateSize
fireRateEnd = fireRate + fireRateSize
evolveRateEnd = evolveRate + evolveRateSize

dataSize = paramSize + fireRateSize + evolveRateSize
fireTransformSize = transformSize(dataSize)
evolveTransformSize = transformSize(dataSize)
"used to access data only in finalize"
fireTransform = dataSize
evolveTransform = dataSize + fireTransformSize
fireTransformEnd = fireTransform + fireTransformSize
evolveTransformEnd = evolveTransform + evolveTransformSize

divisionDataSize = dataSize + fireTransformSize + evolveTransformSize
divisionTransformWidth = divisionDataSize



class Neuron(Cell):
  
  def __init__(self, node, inSynapses, outSynapses, data):
    "structure"
    self.brain = None
    self.inSynapses = set(inSynapses)
    self.outSynapses = set(outSynapses)
    
    "division data"
    self.node = node
    self.data = data
    
    self.fireRate = None
    self.evolveRate = None
    
    "static behavior of all other attributes"
    self.fireTransform = None
    self.evolveTransform = None
    
    "utilities"
    self.inBuffer = 0
    self.nextEvent = None
    self.accessDict = { \
        'sensitivity' : lambda : self.data[sensitivity], \
        'bias' : lambda : self.data[bias], \
        'input' : lambda : self.data[input], \
        'fireRateScale' : lambda : self.data[fireRateScale], \
        'evolveRateScale' : lambda : self.data[evolveRateScale], \
        'params' : lambda : self.data[:paramSize], \
        'fireRateFun' : lambda : self.data[fireRate:fireRateEnd], \
        'evolveRateFun' : lambda : self.data[evolveRate:evolveRateEnd] \
        }
    self.writeDict = { \
        'sensitivity' : self.writeValue(sensitivity), \
        'bias' : self.writeValue(bias), \
        'input' : self.writeValue(input), \
        'fireRateScale' : self.writeValue(fireRateScale), \
        'evolveRateScale' : self.writeValue(evolveRateScale), \
        'params' : lambda : self.writeValue(0, paramSize), \
        'fireRateFun' : self.writeVector(fireRate, fireRateSize), \
        'evolveRateFun' : self.writeVector(evolveRate, evolveRateSize) \
    }
  
  def flush(self):
    self.input += self.sensitivity * (self.inBuffer + self.bias)
    self.inBuffer = 0.0
    self.nextEvent.active = False
    self.schedule()
  
  def fire(self):
    for synapse in self.outSynapses:
      synapse.fire(self)
    for synapse in self.outSynapses:
      synapse.sink.flush()
    self.data += applyTransform(self.data, self.fireTransform)
    self.schedule()
  
  def evolve(self):
    self.data += applyTransform(self.data, self.evolveTransform)
    self.schedule()
  
  "enqueues new events"
  def schedule(self):
    self.updateRates()
    fireDelay = sampleDelay(self.fireRate)
    evolveDelay = sampleDelay(self.evolveRate)
    if (fireDelay < evolveDelay):
      delay = fireDelay
      action = self.fire
    else:
      delay = evolveDelay
      action = self.evolve
    if (delay < inf):
      self.pushEvent(action, self.brain.currentTime + delay)
  
  def updateRates(self):
    self.fireRate = self.fireRateScale * \
        sigmoid(applyTransform(self.params, self.fireRateFun))
    self.evolveRate = self.evolveRateScale * \
        sigmoid(applyTransform(self.params, self.evolveRateFun))
  
  def divide(self):
    "initialize children"
    left = deepcopy(self)
    right = deepcopy(self)
    left.inSynapses = set()
    left.outSynapses = set()
    right.inSynapses = set()
    right.outSynapses = set()
    left.node = self.node.left
    right.node = self.node.right
    
    "create new synapse"
    synapse = self.node.synapse
    left.outSynapses.add(synapse)
    right.inSynapses.add(synapse)
    synapse.source = left
    synapse.sink = right
    
    "carry synapses to children"
    for synapse in self.inSynapses:
      synapse.node = deepcopy(synapse.node)
      branch = synapse.node.sinkCarries[-1]
      synapse.node.sinkCarries.remove[-1]
      if (branch == 0):
        left.inSynapses.add(synapse)
        synapse.source = left
      else:
        right.inSynapses.add(synapse)
        synapse.source = right
    for synapse in self.outSynapses:
      synapse.node = deepcopy(synapse.node)
      branch = synapse.node.sourceCarries[-1]
      synapse.node.sinkCarries.remove[-1]
      if (branch == 0):
        left.outSynapses.add(synapse)
        synapse.sink = left
      else:
        right.outSynapses.add(synapse)
        synapse.sink = right
        
    "apply left and right transforms to the data of left and right"
    left.data = self.data + applyTransform(self.data, self.node.leftTransform)
    right.data = self.data + applyTransform(self.data, self.node.rightTransform)
    
    return ((left, right), synapse)
  
  def finalize(self):
    self.fireTransform = \
        rollTransform(self.data[fireTransform:fireTransformEnd], dataSize)
    self.evolveTransform = \
        rollTransform(self.data[evolveTransform:evolveTransformEnd], dataSize)
    self.data = self.data[:dataSize]
    for synapse in self.outSynapses:
      synapse.finalize()
    self.node = None
  
  "should only be called on a seed neuron"
  def spawn(self):
    synapse = list(self.outSynapses)[0].spawn()
    #data should be mutated.
    child = Neuron(self.node.spawn(), [synapse], [synapse], self.data)
    return child







