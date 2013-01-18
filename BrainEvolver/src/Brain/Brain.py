'''
Created on Dec 26, 2012

@author: Justin
'''

import heapq
from Neuron import Neuron
from Synapse import Synapse
from DivisionTree import *

class Brain(object):
  
  def __init__(self, seed, inputs, outputs, energy):
    self.energy = energy
    self.seed = seed
    self.neurons = set([seed])
    self.inputs = inputs
    self.outputs = outputs
    self.events = heapq()
    
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
  
  "Returns an asexually produced child."
  def spawn(self):
    childSeed = self.seed.spawn()
    return Brain(childSeed, self.inputs, self.outputs)
  
  "Returns a default brain with no evolved structure."
  def createEmpty(self):
    synapse = Synapse(leafSynapseNode, None, None)
    neuron = Neuron(leafNeuronNode, [synapse], [synapse])
    synapse.prev = neuron
    synapse.next = neuron
    return neuron
  
  "Runs until it is in sync with currentTime."
  def updateTime(self, currentTime):
    pass


"takes two brains and returns a child brain"
def breed(a, b):
  pass