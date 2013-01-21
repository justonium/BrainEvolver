'''
Created on Jan 17, 2013

@author: Justin
'''

from Brain import *

from Body.ArrayInterface import *

brain = createEmpty([], [])
#nnode = NeuronNode(leafNeuronNode, leafNeuronNode, False)
#nnode.brain = brain
#brain.seed.node = nnode
#list(brain.seed.outSynapses)[0].node = SynapseNode(leafSynapseNode, leafSynapseNode, False)

brain.elapseTime(1.0)

for i in range(100):
  brain = brain.spawn()

print brain.numNeurons()