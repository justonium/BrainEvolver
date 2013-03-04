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
from DynamicalSystem import *

systemType = Neurons.systemType

numAttributes = 4

"paramSize < dataSize < divisionDataSize"
numChemicals = 4
chemicals = 0
chemicalsEnd = numChemicals

dataSize = numChemicals
fireTransformSize = getParamSize(systemType, dataSize, 2*Neurons.numChemicals)
evolveTransformSize = getParamSize(systemType, dataSize, 2*Neurons.numChemicals)
attributeFunSize = reduceSize(numChemicals)

"used to access data only in finalize"
activationFun = numChemicals
activationFunEnd = activationFun + attributeFunSize
weightFun = activationFunEnd
weightFunEnd = weightFun + transformSize(numChemicals, Neurons.inputSize)
weightFunDim = (Neurons.inputSize, numChemicals + 1)
fireRateFun = weightFunEnd
fireRateFunEnd = fireRateFun + attributeFunSize
evolveRateFun = fireRateFunEnd
evolveRateFunEnd = evolveRateFun + attributeFunSize

fireTransform = evolveRateFunEnd
fireTransformEnd = fireTransform + fireTransformSize
evolveTransform = fireTransformEnd
evolveTransformEnd = evolveTransform + evolveTransformSize

divisionDataSize = dataSize + fireTransformSize + evolveTransformSize + numAttributes*attributeFunSize



class Synapse(Cell):
  
  def copy(self):
    return Synapse(self.node, self.data.copy(), self.brain)
  
  def __init__(self, node, data, brain=None):
    self.finalized = False
    
    "structure"
    self.brain = brain
    self.source = None
    self.sink = None
    
    "division data"
    self.node = node
    self.data = data
    
    "dynamic data"
    self.system = None
    
    self.evolveRate = None
    
    "dynamic behavior of main attributes"
    self.fireTransform = None
    self.evolveTransform = None
    
    "utilities"
    self.nextEvent = None
    
    self.chemicals = None
    
    self.activationFun = None
    self.weightFun = None
    self.fireRateFun = None
    self.evolveRateFun = None
    
    self.activation = None
    self.weight = None
    self.fireRate = None
    self.evolveRate = None
  
  def fire(self, source):
    sink = self.getSink(source)
    sink.inBuffer += self.weight * self.activation
    self.system.step(self.fireTransform, concatenate([sink.chemicals, source.chemicals]))
    self.chemicals = self.system.y
    self.schedule()
    return sink
  
  def getSink(self, source):
    return self.sink if source == self.source else self.source
  
  def evolve(self):
    self.system.step(self.evolveTransform, concatenate((self.source.chemicals, self.sink.chemicals)))
    self.chemicals = self.system.y
    self.schedule()
  
  "enqueues new events"
  def schedule(self):
    if (self.nextEvent is not None):
      self.nextEvent.active = False
    self.updateAttributes()
    delay = sampleDelay(self.evolveRate)
    action = self.evolve
    if (delay < inf):
      self.pushEvent(action, self.source.brain.currentTime + delay)
  
  def updateAttributes(self):
    self.activation = applyTransform(self.chemicals, self.activationFun)
    self.weight = applyTransform(self.chemicals, self.weightFun)
    self.fireRate = applyTransform(self.chemicals, self.fireRateFun)
    self.evolveRate = applyTransform(self.chemicals, self.evolveRateFun)
  
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
    self.finalized = True
    
    if (self.node.symmetric):
      self.sink.inSynapses.remove(self)
      self.sink.outSynapses.add(self)
    
    self.chemicals = self.data[chemicals:chemicalsEnd]
    
    self.activationFun = self.data[activationFun:activationFunEnd]
    self.weightFun = self.data[weightFun:weightFunEnd].reshape(weightFunDim)
    self.fireRateFun = self.data[fireRateFun:fireRateFunEnd]
    self.evolveRateFun = self.data[evolveRateFun:evolveRateFunEnd]
    
    self.system = systemType(dataSize, self.data[:dataSize], 2*Neurons.numChemicals)
    self.fireTransform = self.system.reshapeParams(self.data[fireTransform:fireTransformEnd])
    self.evolveTransform = self.system.reshapeParams(self.data[evolveTransform:evolveTransformEnd])
    
    self.updateAttributes()
    
    self.data = None
    
    "We don't need this node anymore."
    if (self.node.tree is None):
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





