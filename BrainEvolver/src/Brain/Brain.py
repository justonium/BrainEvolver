'''
Created on Dec 26, 2012

@author: Justin
'''

from numpy import *
from heapq import *
import Synapses
from Synapses import Synapse
import Neurons
from Neurons import Neuron, InputNeuron, OutputNeuron
from DivisionTree import *

class Brain(object):
  
  def __init__(self, seed, inputs, outputs, inputNeurons, outputNeurons):
    "These parameters are for outside use."
    self.inputs = inputs
    self.outputs = outputs
    
    self.inputNeurons = inputNeurons
    self.outputNeurons = outputNeurons
    
    self.seed = seed
    self.seed.brain = self
    list(seed.outSynapses)[0].brain = self
    self.currentTime = None
    self.neurons = set([self.seed.copy()])
    self.events = []
    
    openNeurons = set()
    closedNeurons = set()
    openSynapses = set()
    closedSynapses = set()
    for neuron in self.neurons:
      #place neurons in appropriate set
      if (neuron.node.complete):
        closedNeurons.add(neuron)
      else:
        openNeurons.add(neuron)
      #place synapses in appropriate set
      for synapse in neuron.outSynapses:
        if (not synapse.node.complete):
          if (synapse.node.isReady()):
            openSynapses.add(synapse)
          else:
            closedSynapses.add(synapse)
    
    #perform division algorithm
    while (openNeurons):
      #divide relevant synapses
      while (openSynapses):
        for curr in openSynapses.copy():
          openSynapses.remove(curr)
          children = curr.divide()
          for child in children:
            if (not child.node.complete):
              if (child.node.isReady()):
                openSynapses.add(child)
              else:
                closedSynapses.add(child)
      
      #divide all incomplete neurons
      for curr in openNeurons.copy():
        openNeurons.remove(curr)
        children, synapse = neuron.divide()
        for child in children:
          if (child.node.complete):
            closedNeurons.add(child)
          else:
            openNeurons.add(child)
        if (synapse != None and not synapse.node.complete):
          if (synapse.node.isReady()):
            openSynapses.add(synapse)
          else:
            closedSynapses.add(synapse)
    
    self.neurons = closedNeurons
    
    for neuron in self.neurons:
      neuron.finalize()
  
  def _startTime(self):
    self.currentTime = 0.0
    for neuron in self.neurons:
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
    inputNeurons = [neuron.spawn(self.seed.node) for neuron in self.inputNeurons]
    outputNeurons = [neuron.copy() for neuron in self.outputNeurons]
    childSeed = self.seed.spawn()
    return Brain(childSeed, zeros(len(self.inputs)), zeros(len(self.outputs)), \
                 inputNeurons, outputNeurons)



"takes two brains and returns a child brain"
def breed(a, b):
  pass

'''
Returns a default brain with no evolved structure.
inputs and outputs must be lists of some sort (they could be numpy arrays).
'''
def createEmpty(inputs, outputs):
  "Create isolated seed."
  synapse = Synapse(rootSynapseNode(), None, None, zeros(Synapses.divisionDataSize))
  neuron = Neuron(rootNeuronNode(), [synapse], [synapse], zeros(Neurons.divisionDataSize))
  
  "Connect seed to inputs and outputs."
  inputNeurons = [InputNeuron(None, None, None, zeros(Neurons.divisionDataSize)) \
                  for i in range(len(inputs))]
  outputNeurons = [OutputNeuron(None, None, None, zeros(Neurons.divisionDataSize)) \
                   for i in range(len(outputs))]
  
  "Make and start brain."
  brain = Brain(neuron, inputs, outputs, inputNeurons, outputNeurons)
  brain._startTime()
  return brain






