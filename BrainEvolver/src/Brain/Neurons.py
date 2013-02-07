'''
Created on Dec 30, 2012

@author: Justin
'''

try:
  from numpypy import *
except:
  from numpy import *
import random
from heapq import *
from Cell import Cell
import Synapses
import DivisionTree
from Tools import *
from DynamicalSystem import *

systemType = LDS

'''main attributes'''
sensitivity = 0
bias = 1
input = 2
fireRateScale = 3
evolveRateScale = 4
fireRate = 5
evolveRate = 6

"paramSize < dataSize < divisionDataSize"
numAttributes = 7
numChemicals = 1
params = 0
paramSize = numAttributes + numChemicals
chemicals = numAttributes
chemicalsEnd = paramSize

dataSize = paramSize
fireTransformSize = getParamSize(systemType, dataSize)
evolveTransformSize = getParamSize(systemType, dataSize)
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
    '''There will only be 1 synapse, but the circumstances are different for different types
    of neurons, and this loop handles every case.'''
    for synapse in self.inSynapses.union(self.outSynapses):
      child = synapse.copy()
      if (synapse in self.inSynapses):
        inSynapses.add(child)
      if (synapse in self.outSynapses):
        outSynapses.add(child)
    return type(self)(self.node, inSynapses, outSynapses, self.data.copy(), self.brain)
  
  def __init__(self, node, inSynapses, outSynapses, data, brain=None):
    "structure"
    self.brain = brain
    self.inSynapses = set(inSynapses)
    self.outSynapses = set(outSynapses)
    for synapse in inSynapses:
      synapse.sink = self
    for synapse in outSynapses:
      synapse.source = self
    
    "division data"
    self.node = node
    self.data = data
    
    "dynamic data"
    self.system = None
    
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
        'fireRate' : lambda : self.data[fireRate], \
        'evolveRate' : lambda : self.data[evolveRate] \
        }
    self._writeDict = { \
        'sensitivity' : self.writeValue(sensitivity), \
        'bias' : self.writeValue(bias), \
        'input' : self.writeValue(input), \
        'fireRateScale' : self.writeValue(fireRateScale), \
        'evolveRateScale' : self.writeValue(evolveRateScale), \
        'chemicals' : self.writeVector(chemicals, chemicalsEnd), \
        'params' : self.writeVector(params, paramSize), \
        'fireRate' : self.writeValue(fireRate), \
        'evolveRate' : self.writeValue(evolveRate) \
    }
  
  def getSynapse(self):
    raise NotImplementedError
  
  def flush(self):
    self.input += self.sensitivity * (self.inBuffer + self.bias)
    self.inBuffer = 0.0
    self.schedule()
  
  def fire(self):
    nextNeurons = set()
    for synapse in self.outSynapses:
      sink = synapse.fire(self)
      nextNeurons.add(sink)
    for neuron in nextNeurons:
      neuron.flush()
    #self.data += applyTransform(self.data, self.fireTransform)
    self.system.step(self.fireTransform)
    self.data = self.system.y
    self.schedule()
  
  def evolve(self):
    #self.data += applyTransform(self.data, self.evolveTransform)
    self.system.step(self.evolveTransform)
    self.data = self.system.y
    self.schedule()
  
  "enqueues new events"
  def schedule(self):
    "This remains true after self.nextEvent has executed."
    if (self.nextEvent != None):
      self.nextEvent.active = False
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
    '''
    self.fireRate = self.fireRateScale * \
        sigmoid(applyTransform(self.params, self.fireRateFun))
    self.evolveRate = self.evolveRateScale * \
        sigmoid(applyTransform(self.params, self.evolveRateFun))
    '''
    pass
  
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
        branch = random.randint(0, 1)
      if (branch == 0):
        left.inSynapses.add(synapse)
        synapse.sink = left
      else:
        right.inSynapses.add(synapse)
        synapse.sink = right
    for synapse in self.outSynapses:
      synapse.node = synapse.node.copy()
      if (synapse.node.sourceCarries):
        branch = synapse.node.sourceCarries[-1]
        del synapse.node.sourceCarries[-1]
      else:
        branch = random.randint(0, 1)
      if (branch == 0):
        left.outSynapses.add(synapse)
        synapse.source = left
      else:
        right.outSynapses.add(synapse)
        synapse.source = right
        
    "apply left and right transforms to the data of left and right"
    left.data = self.data + applyMap(self.data, self.node.leftTransform)
    right.data = self.data + applyMap(self.data, self.node.rightTransform)
    
    return (left, right)
    
    return ((left, right), synapse)
  
  def finalize(self):
    '''self.fireTransform = \
        rollTransform(self.data[fireTransform:fireTransformEnd], dataSize)
    self.evolveTransform = \
        rollTransform(self.data[evolveTransform:evolveTransformEnd], dataSize)'''
    
    self.system = systemType(dataSize, self.data[:dataSize])
    self.fireTransform = self.system.reshapeParams(self.data[fireTransform:fireTransformEnd])
    self.evolveTransform = self.system.reshapeParams(self.data[evolveTransform:evolveTransformEnd])
    
    self.data = self.data[:dataSize]
    "We don't need this node anymore."
    #if (self.node.tree == None):
      #self.node = None
  
  "should only be called on a seed neuron"
  def spawn(self):
    inSynapses = set()
    outSynapses = set()
    for synapse in self.inSynapses.intersection(self.outSynapses):
      child = synapse.spawn()
      if (synapse in self.inSynapses):
        inSynapses.add(child)
      if (synapse in self.outSynapses):
        outSynapses.add(child)
    data = self.node.tree.mutateData(self.data)
    child = Neuron(self.node.spawn(), inSynapses, outSynapses, data)
    return child


class InputNeuron(Neuron):
  
  def getSynapse(self):
    return list(self.outSynapses)[0]
  
  def updateRates(self):
    input = self.input
    super(InputNeuron, self).updateRates()
    self.input = input
  
  def spawn(self, tree):
    synapse = self.getSynapse().spawn()
    data = tree.mutateData(self.data)
    child = InputNeuron(None, [], [synapse], data)
    return child

class OutputNeuron(Neuron):
  
  def getSynapse(self):
    return list(self.inSynapses)[0]
  
  def spawn(self, tree):
    synapse = self.getSynapse().spawn()
    data = tree.mutateData(self.data)
    child = OutputNeuron(None, [synapse], [], data)
    return child
  
  def finalize(self):
    self.data = self.data[:dataSize]
  
  def fire(self):
    pass
  
  def evolve(self):
    pass
  
  def schedule(self):
    pass



def defaultNeuronTransform():
  return zeros((2, divisionDataSize))

def createRootNeuron(inSynapses, outSynapses):
  return Neuron(DivisionTree.rootNeuronNode(), inSynapses, outSynapses, zeros(divisionDataSize))




