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

systemType = CTRNN

numAttributes = 4

"paramSize < dataSize < divisionDataSize"
inputSize = 1
numChemicals = inputSize + 4
chemicals = 0
chemicalsEnd = numChemicals

dataSize = numChemicals
fireTransformSize = getParamSize(systemType, dataSize)
evolveTransformSize = getParamSize(systemType, dataSize)
inputFireTransformSize = getParamSize(systemType, dataSize, 1) #unused
inputEvolveTransformSize = getParamSize(systemType, dataSize, 1) #unused
attributeFunSize = reduceSize(numChemicals)

"used to access data only in finalize"
sensitivityFun = dataSize
sensitivityFunEnd = sensitivityFun + attributeFunSize
biasFun = sensitivityFunEnd
biasFunEnd = biasFun + attributeFunSize
fireRateFun = biasFunEnd
fireRateFunEnd = fireRateFun + attributeFunSize
evolveRateFun = fireRateFunEnd
evolveRateFunEnd = evolveRateFun + attributeFunSize

fireTransform = evolveRateFunEnd
fireTransformEnd = fireTransform + fireTransformSize
evolveTransform = fireTransformEnd
evolveTransformEnd = evolveTransform + evolveTransformSize

inputFireTransform = evolveRateFunEnd
inputFireTransformEnd = inputFireTransform + inputFireTransformSize
inputEvolveTransform = inputFireTransformEnd
inputEvolveTransformEnd = inputEvolveTransform + inputEvolveTransformSize

divisionDataSize = dataSize + fireTransformSize + evolveTransformSize + numAttributes*attributeFunSize
inputDivisionDataSize = dataSize + inputFireTransformSize + inputEvolveTransformSize \
    + numAttributes*attributeFunSize



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
    self.finalized = False
    
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
    
    self.chemicals = None
    
    self.sensitivityFun = None
    self.biasFun = None
    self.inputFun = None
    self.fireRateFun = None
    self.evolveRateFun = None
    
    self.sensitivity = None
    self.bias = None
    self.input = None
    self.fireRate = None
    self.evolveRate = None
  
  def _setInput(self, input):
    if (input is not None and not isinstance(input, ndarray)):
        raise TypeError
    self.__input = input
  def _getInput(self):
    return self.__input
  input = property(_getInput, _setInput)
  
  def getSynapse(self):
    raise NotImplementedError
  
  "inBuffer and input are both buffers in members of Neuron and OutputNeuron."
  def flush(self):
    #debug
    if (self.sensitivity == 1):
      pass
    
    self.input += self.sensitivity * (self.inBuffer + self.bias)
    self.inBuffer = 0.0
    self.feedInput()
    self.schedule()
  
  def fire(self):
    self.feedInput()
    nextNeurons = set()
    for synapse in self.outSynapses:
      sink = synapse.fire(self)
      nextNeurons.add(sink)
    for neuron in nextNeurons:
      neuron.flush()
    self.system.step(self.fireTransform)
    self.chemicals = self.system.y
    self.schedule()
    
  
  def evolve(self):
    #debug
    if (self.evolveTransform[1][0] == 1):
      pass
    
    self.feedInput()
    self.system.step(self.evolveTransform)
    self.chemicals = self.system.y
    self.schedule()
  
  "enqueues new events"
  def schedule(self):
    "This remains true after self.nextEvent has executed."
    if (self.nextEvent is not None):
      self.nextEvent.active = False
    self.updateAttributes()
    fireDelay = sampleDelay(self.fireRate)
    #pickle.dump(self, open('./testnetwork.pkl', 'wb'))
    evolveDelay = sampleDelay(self.evolveRate)
    if (fireDelay < evolveDelay):
      delay = fireDelay
      action = self.fire
    else:
      delay = evolveDelay
      action = self.evolve
    if (delay < inf):
      self.pushEvent(action, self.brain.currentTime + delay)
  
  def updateAttributes(self):
    self.sensitivity = applyTransform(self.chemicals, self.sensitivityFun)
    self.bias = applyTransform(self.chemicals, self.biasFun)
    self.fireRate = applyTransform(self.chemicals, self.fireRateFun)
    self.evolveRate = applyTransform(self.chemicals, self.evolveRateFun)
  
  def feedInput(self):
    self.system.feedInput(self.input)
    self.input = zeros(inputSize)
    self.chemicals = self.system.y
  
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
    self.finalized = True
    
    self.chemicals = self.data[chemicals:chemicalsEnd]
    
    self.sensitivityFun = self.data[sensitivityFun:sensitivityFunEnd]
    self.biasFun = self.data[biasFun:biasFunEnd]
    self.fireRateFun = self.data[fireRateFun:fireRateFunEnd]
    self.evolveRateFun = self.data[evolveRateFun:evolveRateFunEnd]
    
    self.system = systemType(dataSize, self.data[:dataSize])
    self.fireTransform = self.system.reshapeParams(self.data[fireTransform:fireTransformEnd])
    self.evolveTransform = self.system.reshapeParams(self.data[evolveTransform:evolveTransformEnd])
    
    self.input = zeros(inputSize)
    self.updateAttributes()
    
    #debug
    if (self.data[evolveTransform + dataSize * (dataSize + 1)] == 1):
      pass
    
    self.data = None
    
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
  
  def sanity(self):
    if (not (self.finalized \
        and self.sensitivity is not None \
        and self.bias is not None \
        and self.input is not None \
        and type(self.input) == ndarray)):
      print 'fail'


class InputNeuron(Neuron):
  
  def __init__(self, node, inSynapses, outSynapses, data, tree, brain=None):
    super(type(self), self).__init__(node, inSynapses, outSynapses, data, brain)
    self.tree = tree
  
  def getSynapse(self):
    return list(self.outSynapses)[0]
  
  def flush(self):
    pass
  
  def fire(self):
    nextNeurons = set()
    for synapse in self.outSynapses:
      sink = synapse.fire(self)
      nextNeurons.add(sink)
    for neuron in nextNeurons:
      neuron.flush()
    self.system.step(self.fireTransform, self.input)
    self.chemicals = self.system.y
    self.schedule()
  
  def evolve(self):
    #debug
    if (self.evolveTransform[1][0] == 1):
      pass
    
    self.system.step(self.evolveTransform, self.input)
    self.chemicals = self.system.y
    self.schedule()
  
  def spawn(self):
    synapse = self.getSynapse().spawn()
    data = self.tree.mutateData(self.data)
    child = InputNeuron(None, [], [synapse], data, self.tree.spawn(None))
    return child
  
  def finalize(self):
    self.finalized = True
    
    self.chemicals = self.data[chemicals:chemicalsEnd]
    
    self.sensitivityFun = self.data[sensitivityFun:sensitivityFunEnd]
    self.biasFun = self.data[biasFun:biasFunEnd]
    self.fireRateFun = self.data[fireRateFun:fireRateFunEnd]
    self.evolveRateFun = self.data[evolveRateFun:evolveRateFunEnd]
    
    self.system = systemType(dataSize, self.data[:dataSize], 1)
    self.fireTransform = self.system.reshapeParams(self.data[inputFireTransform:inputFireTransformEnd])
    self.evolveTransform = \
        self.system.reshapeParams(self.data[inputEvolveTransform:inputEvolveTransformEnd])
    
    self.input = zeros(1)
    self.updateAttributes()
    
    #debug
    if (self.data[inputEvolveTransform + dataSize * (dataSize + 2)] == 1):
      pass
    
    self.data = None

class OutputNeuron(Neuron):
  
  def getSynapse(self):
    return list(self.inSynapses)[0]
  
  def spawn(self, tree):
    synapse = self.getSynapse().spawn()
    data = tree.mutateData(self.data)
    child = OutputNeuron(None, [synapse], [], data)
    return child



def defaultNeuronTransform():
  return zeros((2, divisionDataSize))

def createRootNeuron(inSynapses, outSynapses):
  return Neuron(DivisionTree.rootNeuronNode(), inSynapses, outSynapses, zeros(divisionDataSize))




