'''
Created on Jan 15, 2013

@author: Justin
'''

from Brain import *

brain = createEmpty([], [])
#nnode = NeuronNode(leafNeuronNode, leafNeuronNode, False)
#nnode.brain = brain
#brain.seed.node = nnode
#list(brain.seed.outSynapses)[0].node = SynapseNode(leafSynapseNode, leafSynapseNode, False)

brain.elapseTime(1.0)

brain2 = brain.spawn()