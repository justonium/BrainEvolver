'''
Created on Jan 17, 2013

@author: Justin
'''

import Brain
from Brain import Neuron
from Brain import Synapse

from Brain import *

brain = createEmpty(range(1), range(1))
#nnode = NeuronNode(leafNeuronNode, leafNeuronNode, False)
#nnode.brain = brain
#brain.seed.node = nnode
#list(brain.seed.outSynapses)[0].node = SynapseNode(leafSynapseNode, leafSynapseNode, False)

for i in range(100):
  brain = brain.spawn()
  print 'generation: ', i
  print 'number of neurons: ', brain.numNeurons()
  print 'number of synapses: ', brain.numSynapses()
  brain.elapseTime(1.0, range(1))
  print 'outputs: ', brain.outputs