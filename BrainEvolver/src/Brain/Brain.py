'''
Created on Dec 26, 2012

@author: Justin
'''

from numpy import *
from heapq import *
from DivisionTree import *
import Synapses
from Synapses import Synapse
import Neurons
from Neurons import Neuron, InputNeuron, OutputNeuron

class Brain(object):
  
  def __init__(self, seed, inputs, outputs, inputNeurons, outputNeurons):
    "These parameters are for outside use."
    self.inputs = inputs
    self.outputs = outputs
    
    "It is unnecessary to keep outputNeuronArchive so long as outputNeuron is hollow."
    self.inputNeuronArchive = inputNeurons
    self.outputNeuronArchive = outputNeurons
    self.inputNeurons = [neuron.copy() for neuron in inputNeurons]
    self.outputNeurons = [neuron.copy() for neuron in outputNeurons]
    
    self.seed = seed
    self.seed.brain = self
    "This is ok since there is only 1 synapse on the seed."
    for synapse in self.seed.outSynapses:
      synapse.brain = self
    for neuron in self.inputNeurons:
      neuron.brain = self
      neuron.finalize()
    for neuron in self.outputNeurons:
      neuron.brain = self
      neuron.finalize()
    
    self.currentTime = None
    self.events = []
    divideNeuron = self.seed.copy()
    self.neurons = set([divideNeuron])
    
    "Connect inputs and outputs to the single neuron before it divides."
    for neuron in self.inputNeurons:
      synapse = list(neuron.outSynapses)[0]
      synapse.sink = divideNeuron
      divideNeuron.inSynapses.add(synapse)
    for neuron in self.outputNeurons:
      synapse = list(neuron.inSynapses)[0]
      synapse.source = divideNeuron
      divideNeuron.outSynapses.add(synapse)
    
    openNeurons = set()
    closedNeurons = set()
    openSynapses = set()
    closedSynapses = set()
    for neuron in self.neurons:
      "place neurons in appropriate set"
      if (neuron.node.complete):
        closedNeurons.add(neuron)
      else:
        openNeurons.add(neuron)
      "place synapses in appropriate set"
      for synapse in neuron.outSynapses:
        if (not synapse.node.complete):
          if (synapse.isReady()):
            openSynapses.add(synapse)
          else:
            closedSynapses.add(synapse)
    
    "perform division algorithm"
    while (openNeurons):
      "divide relevant synapses"
      while (openSynapses):
        for curr in openSynapses.copy():
          openSynapses.remove(curr)
          children = curr.divide()
          for child in children:
            if (not child.node.complete):
              if (child.isReady()):
                openSynapses.add(child)
              else:
                closedSynapses.add(child)
      
      "divide all incomplete neurons"
      for curr in openNeurons.copy():
        openNeurons.remove(curr)
        children = curr.divide()
        for child in children:
          if (child.node.complete):
            closedNeurons.add(child)
          else:
            openNeurons.add(child)
    
    self.neurons = closedNeurons
    
    for neuron in self.neurons:
      neuron.finalize()
  
  def _startTime(self):
    self.currentTime = 0.0
    for neuron in self.neurons.union(self.inputNeurons):
      neuron.schedule()
      for synapse in neuron.outSynapses:
        synapse.schedule()
  
  "Runs until it is in sync with currentTime."
  def elapseTime(self, timeElapsed, inputs=None):
    "Update input neurons."
    if (inputs == None):
      inputs = self.inputs
    else:
      self.inputs = inputs
      for i in range(len(inputs)):
        self.inputNeurons[i].fireRate = inputs[i]
    self.outputs = 0*self.outputs
    
    "Let the network compute."
    self.currentTime += timeElapsed
    while (self.events and self.events[0].executionTime < self.currentTime):
      event = heappop(self.events)
      if (event.active):
        event.execute()
    
    "Read output neurons."
    for i in range(len(self.outputs)):
      self.outputs[i] = self.outputNeurons[i].input
  
  "Returns an asexually produced child."
  def spawn(self):
    childSeed = self.seed.spawn()
    
    inputNeurons = [neuron.spawn(self.seed.node.tree) for neuron in self.inputNeuronArchive]
    outputNeurons = [neuron.copy() for neuron in self.outputNeuronArchive]
    child = Brain(childSeed, zeros(len(self.inputs)), zeros(len(self.outputs)), \
                 inputNeurons, outputNeurons)
    child._startTime()
    return child
  
  '''
  Returns the number of neurons in the brain.
  This doesn't include input neurons or output neurons, whose numbers
  are equal to the sizes of the corresponding input and output arrays.
  '''
  def numNeurons(self):
    return self.seed.node.treeSize()
  
  '''
  This includes, but is not limited to, the input and output synapses.
  '''
  def numSynapses(self):
    return sum(map(lambda synapse : synapse.node.treeSize(), \
                  list(self.seed.inSynapses.union(self.seed.outSynapses))))
  
  def numInputSynapses(self):
    return sum(map(lambda neuron : list(neuron.outSynapses)[0].node.treeSize(), self.inputNeurons))
  
  def numOutputSynapses(self):
    return sum(map(lambda neuron : list(neuron.inSynapses)[0].node.treeSize(), self.outputNeurons))


"takes two brains and returns a child brain"
def breed(a, b):
  pass

'''
Returns a default brain with no evolved structure.
inputs and outputs must be lists of some sort (they could be numpy arrays).
'''
def createEmpty(inputs, outputs):
  "Create isolated seed."
  synapse = Synapses.createRootSynapse()
  seed = Neurons.createRootNeuron([synapse], [synapse])
  
  inputSynapses = [Synapses.createRootSynapse() for i in range(len(inputs))]
  outputSynapses = [Synapses.createRootSynapse() for i in range(len(outputs))]
  
  "Connect seed to inputs and outputs."
  inputNeurons = [InputNeuron(None, [], [inputSynapses[i]], zeros(Neurons.divisionDataSize)) \
                  for i in range(len(inputs))]
  outputNeurons = [OutputNeuron(None, [outputSynapses[i]], [], zeros(Neurons.divisionDataSize)) \
                   for i in range(len(outputs))]
  
  "Make and start brain."
  brain = Brain(seed, inputs, outputs, inputNeurons, outputNeurons)
  brain._startTime()
  return brain






