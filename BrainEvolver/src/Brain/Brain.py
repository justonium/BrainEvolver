'''
Created on Dec 26, 2012

@author: Justin
'''

from numpy import *
from heapq import *
import Synapses
from Synapses import Synapse
import Neurons
from Neurons import Neuron
from DivisionTree import *

class Brain(object):
  
  def __init__(self, seed, inputs, outputs, energy):
    seed.brain = self
    list(seed.outSynapses)[0].brain = self
    self.energy = energy
    self.currentTime = None
    self.seed = seed
    self.neurons = set([seed])
    self.inputs = inputs
    self.outputs = outputs
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
          if (not synapse.node.sourceCarries and not synapse.node.sinkCarries):
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
              if (not child.node.sourceCarries and not child.node.sinkCarries):
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
          if (not synapse.node.sourceCarries and not synapse.node.sinkCarries):
            openSynapses.add(synapse)
          else:
            closedSynapses.add(synapse)
    
    self.neurons = closedNeurons
    
    for neuron in self.neurons:
      neuron.finalize()
  
  "Returns an asexually produced child."
  def spawn(self):
    childSeed = self.seed.spawn()
    return Brain(childSeed, self.inputs, self.outputs)
  
  def startTime(self):
    self.currentTime = 0.0
    for neuron in self.neurons:
      neuron.schedule()
      for synapse in neuron.outSynapses:
        synapse.schedule()
  
  "Runs until it is in sync with currentTime."
  def elapseTime(self, timeElapsed):
    self.currentTime += timeElapsed
    while (self.events and self.events[0].executionTime < self.currentTime):
      event = heappop(self.events)
      if (event.active):
        event.execute()



"takes two brains and returns a child brain"
def breed(a, b):
  pass

"Returns a default brain with no evolved structure."
def createEmpty(inputs, outputs, energy):
  synapse = Synapse(leafSynapseNode, None, None, zeros(Synapses.divisionDataSize))
  neuron = Neuron(leafNeuronNode, [synapse], [synapse], zeros(Neurons.divisionDataSize))
  synapse.prev = neuron
  synapse.next = neuron
  brain = Brain(neuron, inputs, outputs, energy)
  brain.startTime()
  return brain






