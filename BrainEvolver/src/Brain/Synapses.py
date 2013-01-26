'''
Created on Dec 30, 2012

@author: Justin
'''

try:
  from numpypy import *
except:
  from numpy import *
from heapq import *
from Cell import Cell
import Neurons
from Neurons import Neuron
import DivisionTree
from Tools import *

"main attributes"
activation = 0
weight = 1
evolveRateScale = 2

"paramSize < dataSize < divisionDataSize"
numAttributes = 3
numChemicals = 1
params = 0
paramSize = numAttributes + numChemicals
chemicals = numAttributes
chemicalsEnd = paramSize

evolveRateSize = reduceSize(paramSize)
"also used to access data"
evolveRate = paramSize
evolveRateEnd = evolveRate + evolveRateSize

dataSize = paramSize + evolveRateSize
fireTransformWidth = dataSize + 2*Neurons.numChemicals
evolveTransformWidth = dataSize + 2*Neurons.numChemicals
fireTransformSize = transformSize(fireTransformWidth, dataSize)
evolveTransformSize = transformSize(fireTransformWidth, dataSize)
"used to access data only in finalize"
fireTransform = dataSize
evolveTransform = dataSize + fireTransformSize
fireTransformEnd = fireTransform + fireTransformSize
evolveTransformEnd = evolveTransform + evolveTransformSize

divisionDataSize = dataSize + fireTransformSize + evolveTransformSize



class Synapse(Cell):
  
  def copy(self):
    return Synapse(self.node, self.data.copy(), self.brain)
  
  def __init__(self, node, data, brain=None):
    "structure"
    self.brain = brain
    self.source = None
    self.sink = None
    
    "division data"
    self.node = node
    self.data = data
    
    self.evolveRate = None
    
    "dynamic behavior of main attributes"
    self.fireTransform = None
    self.evolveTransform = None
    
    "utilities"
    self.nextEvent = None
    self._accessDict = { \
        'activation' : lambda : self.data[activation], \
        'weight' : lambda : self.data[weight], \
        'evolveRateScale' : lambda : self.data[evolveRateScale], \
        'chemicals' : lambda : self.data[chemicals:chemicalsEnd], \
        'params' : lambda : self.data[params:paramSize], \
        'evolveRateFun' : lambda : self.data[evolveRate:evolveRateEnd] \
        }
    self._writeDict = { \
        'activation' : super(Synapse, self).writeValue(activation), \
        'weight' : self.writeValue(weight), \
        'evolveRateScale' : self.writeValue(evolveRateScale), \
        'chemicals' : self.writeVector(chemicals, chemicalsEnd), \
        'params' : self.writeVector(params, paramSize), \
        'evolveRateFun' : self.writeVector(evolveRate, evolveRateSize) \
        }
  
  def fire(self, source):
    sink = self.getSink(source)
    sink.inBuffer += self.weight * self.activation
    transformParam = concatenate((self.data, source.chemicals, sink.chemicals))
    self.data += applyTransform(transformParam, self.fireTransform)
    self.schedule()
    return sink
  
  def getSink(self, source):
    return self.sink if source == self.source else self.source
  
  def evolve(self):
    transformParam = concatenate((self.data, self.source.chemicals, self.sink.chemicals))
    self.data += applyTransform(transformParam, self.evolveTransform)
    self.schedule()
  
  "enqueues new events"
  def schedule(self):
    if (self.nextEvent != None):
      self.nextEvent.active = False
    self.updateRates()
    delay = sampleDelay(self.evolveRate)
    action = self.evolve
    if (delay < inf):
      self.pushEvent(action, self.source.brain.currentTime + delay)
  
  def updateRates(self):
    '''
    self.evolveRate = self.evolveRateScale * \
        sigmoid(applyTransform(self.params, self.evolveRateFun))
    '''
    pass
  
  def divide(self):
    left = self.copy()
    right = self.copy()
    left.node = self.node.left
    right.node = self.node.right
    "apply left and right transforms to the data of left and right"
    left.data = self.data + applyMap(self.data, self.node.leftTransform)
    right.data = self.data + applyMap(self.data, self.node.rightTransform)
    
    return (left, right)
  
  def finalize(self):
    if (self.node.symmetric):
      self.sink.inSynapses.remove(self)
      self.sink.outSynapses.add(self)
    self.fireTransform = \
        rollTransform(self.data[fireTransform:fireTransformEnd], fireTransformWidth, dataSize)
    self.evolveTransform = \
        rollTransform(self.data[evolveTransform:evolveTransformEnd], evolveTransformWidth, dataSize)
    self.data = self.data[:dataSize]
    "We don't need this node anymore."
    if (self.node.tree == None):
      self.node = None
  
  def isReady(self):
    sourceComplete = self.source.node.complete if type(self.source) == Neuron else False
    sinkComplete = self.sink.node.complete if type(self.sink) == Neuron else False
    return not (self.node.sourceCarries and not sourceComplete \
      or self.node.sinkCarries and not sinkComplete)
  
  "Should only be called on a root."
  def spawn(self):
    data = self.node.tree.mutateData(self.data)
    return Synapse(self.node.spawn(), data)



def defaultSynapseTransform():
  return zeros((2, divisionDataSize))

def createRootSynapse():
  return Synapse(DivisionTree.rootSynapseNode(), zeros(divisionDataSize))





