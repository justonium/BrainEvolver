'''
Created on Dec 30, 2012

@author: Justin
'''
from numpy import *
from heapq import *
from Cell import Cell
import Synapses
import DivisionTree
from Tools import *

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
chemicals = numAttributes
chemicalsEnd = paramSize

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



class Neuron(Cell):
  
  def copy(self):
    inSynapses = set()
    outSynapses = set()
    for synapse in self.inSynapses.union(self.outSynapses):
      child = synapse.copy()
      if (synapse in self.inSynapses):
        inSynapses.add(child)
      if (synapse in self.outSynapses):
        outSynapses.add(child)
    return Neuron(self.node, inSynapses, outSynapses, self.data.copy())
  
  def __init__(self, node, inSynapses, outSynapses, data):
    "structure"
    self.brain = None
    self.inSynapses = set(inSynapses)
    self.outSynapses = set(outSynapses)
    for synapse in inSynapses:
      synapse.sink = self
    for synapse in outSynapses:
      synapse.source = self
    
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
    self._accessDict = { \
        'sensitivity' : lambda : self.data[sensitivity], \
        'bias' : lambda : self.data[bias], \
        'input' : lambda : self.data[input], \
        'fireRateScale' : lambda : self.data[fireRateScale], \
        'evolveRateScale' : lambda : self.data[evolveRateScale], \
        'chemicals' : lambda : self.data[chemicals:chemicalsEnd], \
        'params' : lambda : self.data[params:paramSize], \
        'fireRateFun' : lambda : self.data[fireRate:fireRateEnd], \
        'evolveRateFun' : lambda : self.data[evolveRate:evolveRateEnd] \
        }
    self._writeDict = { \
        'sensitivity' : self.writeValue(sensitivity), \
        'bias' : self.writeValue(bias), \
        'input' : self.writeValue(input), \
        'fireRateScale' : self.writeValue(fireRateScale), \
        'evolveRateScale' : self.writeValue(evolveRateScale), \
        'chemicals' : self.writeVector(chemicals, chemicalsEnd), \
        'params' : self.writeVector(params, paramSize), \
        'fireRateFun' : self.writeVector(fireRate, fireRateEnd), \
        'evolveRateFun' : self.writeVector(evolveRate, evolveRateEnd) \
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
    "This copying business isn't so fast."
    left = self.copy()
    right = self.copy()
    left.inSynapses = set()
    left.outSynapses = set()
    right.inSynapses = set()
    right.outSynapses = set()
    left.node = self.node.left
    right.node = self.node.right
    
    "carry synapses to children"
    for synapse in self.inSynapses:
      synapse.node = synapse.node.copy()
      if (synapse.node.sinkCarries):
        branch = synapse.node.sinkCarries[-1]
        del synapse.node.sinkCarries[-1]
      else:
        branch = random.random_integers(0, 1)
      if (branch == 0):
        left.inSynapses.add(synapse)
        synapse.source = left
      else:
        right.inSynapses.add(synapse)
        synapse.source = right
    for synapse in self.outSynapses:
      synapse.node = synapse.node.copy()
      if (synapse.node.sourceCarries):
        branch = synapse.node.sourceCarries[-1]
        del synapse.node.sourceCarries[-1]
      else:
        branch = random.random_integers(0, 1)
      if (branch == 0):
        left.outSynapses.add(synapse)
        synapse.sink = left
      else:
        right.outSynapses.add(synapse)
        synapse.sink = right
        
    "apply left and right transforms to the data of left and right"
    left.data = self.data + applyMap(self.data, self.node.leftTransform)
    right.data = self.data + applyMap(self.data, self.node.rightTransform)
    
    return (left, right)
    
    return ((left, right), synapse)
  
  def finalize(self):
    self.fireTransform = \
        rollTransform(self.data[fireTransform:fireTransformEnd], dataSize)
    self.evolveTransform = \
        rollTransform(self.data[evolveTransform:evolveTransformEnd], dataSize)
    self.data = self.data[:dataSize]
    for synapse in self.outSynapses:
      synapse.finalize()
    "We don't need this node anymore."
    if (self.node.tree == None):
      self.node = None
  
  "should only be called on a seed neuron"
  def spawn(self):
    inSynapses = set()
    outSynapses = set()
    for synapse in self.inSynapses.union(self.outSynapses):
      child = synapse.spawn()
      if (synapse in self.inSynapses):
        inSynapses.add(child)
      if (synapse in self.outSynapses):
        outSynapses.add(child)
    data = self.node.tree.mutateData(self.data)
    child = Neuron(self.node.spawn(), inSynapses, outSynapses, data)
    return child


class InputNeuron(Neuron):
  
  def __init__(self, node, inSynapses, outSynapses, data):
    super(InputNeuron, self).__init__(node, inSynapses, outSynapses, data)
  
  def updateRates(self):
    fireRate = self.fireRate
    super(InputNeuron, self).updateRates()
    self.fireRate = fireRate
  
  def spawn(self, node):
    inSynapses = set()
    outSynapses = self.outSynapses
    data = node.tree.mutateData(self.data)
    child = InputNeuron(None, inSynapses, outSynapses, data)
    return child

class OutputNeuron(Neuron):
  
  def fire(self):
    pass
  
  def evolve(self):
    pass



def defaultNeuronTransform():
  return zeros((2, divisionDataSize))

def createRootNeuron(inSynapses, outSynapses):
  return Neuron(DivisionTree.rootNeuronNode(), inSynapses, outSynapses, zeros(divisionDataSize))




