'''
Created on Jan 17, 2013

@author: Justin
'''

import Brain
from Brain import Neuron
from Brain import Synapse
from Brain import *

brain = createEmpty(1, 1)
#nnode = NeuronNode(leafNeuronNode, leafNeuronNode, False)
#nnode.brain = brain
#brain.seed.node = nnode
#list(brain.seed.outSynapses)[0].node = SynapseNode(leafSynapseNode, leafSynapseNode, False)

for i in range(100):
  brain = brain.spawn()
  print 'generation: ', i
  print 'number of neurons: ', brain.numNeurons()
  print 'number of synapses: ', brain.numSynapses()
  brain.elapseTime(10.0, [10.])
  print 'outputs: ', brain.outputs