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
  
  def __init__(self, seed, numInputs, numOutputs, inputNeurons, outputNeurons):
    "These parameters are for outside use."
    self.numInputs = numInputs
    self.numOutputs = numOutputs
    self.inputs = zeros(self.numInputs)
    self.outputs = zeros(self.numOutputs)
    
    "keep the provided seed and input and output neurons unaltered"
    "It is unnecessary to keep outputNeuronArchive so long as outputNeuron is hollow."
    self.seed = seed
    self.inputNeuronArchive = inputNeurons
    self.outputNeuronArchive = outputNeurons
    
    "make new copies of the provided seed and input and output neurons for use."
    divideNeuron = self.seed.copy()
    self.inputNeurons = [neuron.copy() for neuron in inputNeurons]
    self.outputNeurons = [neuron.copy() for neuron in outputNeurons]
    
    "Give reference to this brain to all of its components before they divide."
    divideNeuron.brain = self
    "This is ok since there is only 1 synapse on the seed."
    for synapse in divideNeuron.outSynapses:
      synapse.brain = self
    for neuron in self.inputNeurons:
      neuron.brain = self
      neuron.getSynapse().brain = self
    for neuron in self.outputNeurons:
      neuron.brain = self
      neuron.getSynapse().brain = self
    
    self.currentTime = None
    self.events = []
    
    "Connect inputs and outputs to the single neuron before it divides."
    for neuron in self.inputNeurons:
      synapse = neuron.getSynapse()
      synapse.sink = divideNeuron
      divideNeuron.inSynapses.add(synapse)
    for neuron in self.outputNeurons:
      synapse = neuron.getSynapse()
      synapse.source = divideNeuron
      divideNeuron.outSynapses.add(synapse)
    
    openNeurons = set()
    closedNeurons = set()
    openSynapses = set()
    closedSynapses = set()
    "place neuron in appropriate set"
    if (divideNeuron.node.complete):
      closedNeurons.add(divideNeuron)
    else:
      openNeurons.add(divideNeuron)
    "place synapses in appropriate set"
    "This operation is overkill since there is only one synapse."
    for synapse in divideNeuron.outSynapses.union(divideNeuron.inSynapses):
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
    
    "Finalize all neurons."
    for neuron in self.neurons:
      neuron.finalize()
    for neuron in self.inputNeurons:
      neuron.finalize()
    for neuron in self.outputNeurons:
      neuron.finalize()
    
    "Finalize all synapses."
    synapses = set()
    for neuron in self.inputNeurons:
      synapses.add(neuron.getSynapse())
    for neuron in self.neurons:
      synapses.update(neuron.inSynapses)
      synapses.update(neuron.outSynapses)
    '''
    for synapse in synapses:
      sink = synapse.sink
      source = synapse.source
      if (synapse not in sink.inSynapses):
        print 'fail'
      if (synapse not in source.outSynapses):
        print 'fail'
    '''
    for synapse in synapses:
      synapse.finalize()
  
  def _startTime(self):
    self.currentTime = 0.0
    for i in range(self.numInputs):
      neuron = self.inputNeurons[i]
      neuron.input = self.inputs[i]
      neuron.schedule()
    for neuron in self.neurons:
      neuron.schedule()
      for synapse in neuron.outSynapses:
        "In the case of bidirectional synapses, this check prevents double scheduling."
        if (synapse.nextEvent == None):
          synapse.schedule()
  
  '''Runs until it is in sync with currentTime. If no inputs are provided,
  inputs will retain last assigned value.'''
  def elapseTime(self, timeElapsed, inputs=None):
    "Update input neurons."
    if (inputs == None):
      inputs = self.inputs
    else:
      self.inputs = inputs
      for i in range(self.numInputs):
        neuron = self.inputNeurons[i]
        neuron.input = inputs[i]
        neuron.schedule()
        
    self.outputs = 0*self.outputs
    
    "Calculate the final time."
    finalTime = self.currentTime + timeElapsed
    "Let the network compute."
    while (self.events and self.events[0][0] < finalTime):
      executionTime, event = heappop(self.events)
      if (event.active):
        event.execute()
        self.currentTime = executionTime
    self.currentTime = finalTime
    
    "Read output neurons."
    for i in range(self.numOutputs):
      self.outputs[i] = self.outputNeurons[i].input
  
  "Returns an asexually produced child."
  def spawn(self):
    childSeed = self.seed.spawn()
    
    inputNeurons = [neuron.spawn(self.seed.node.tree) for neuron in self.inputNeuronArchive]
    outputNeurons = [neuron.spawn(self.seed.node.tree) for neuron in self.outputNeuronArchive]
    
    child = Brain(childSeed, self.numInputs, self.numOutputs, \
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
    return sum(map(lambda neuron : neuron.getSynapse().node.treeSize(), self.inputNeurons))
  
  def numOutputSynapses(self):
    return sum(map(lambda neuron : neuron.getSynapse().node.treeSize(), self.outputNeurons))


"takes two brains and returns a child brain"
def breed(a, b):
  pass

'''
Returns a default brain with no evolved structure.
inputs and outputs must be lists of some sort (they could be numpy arrays).
'''
def createEmpty(numInputs, numOutputs):
  "Create isolated seed."
  synapse = Synapses.createRootSynapse()
  seed = Neurons.createRootNeuron([synapse], [synapse])
  
  inputSynapses = [Synapses.createRootSynapse() for i in range(numInputs)]
  outputSynapses = [Synapses.createRootSynapse() for i in range(numOutputs)]
  
  "Connect seed to inputs and outputs."
  inputNeurons = [InputNeuron(None, [], [inputSynapses[i]], zeros(Neurons.divisionDataSize)) \
                  for i in range(numInputs)]
  outputNeurons = [OutputNeuron(None, [outputSynapses[i]], [], zeros(Neurons.divisionDataSize)) \
                   for i in range(numOutputs)]
  
  "Make and start brain."
  brain = Brain(seed, numInputs, numOutputs, inputNeurons, outputNeurons)
  brain._startTime()
  return brain






