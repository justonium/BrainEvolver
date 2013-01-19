'''
Created on Jan 15, 2013

@author: Justin
'''

from Brain import *

brain = createEmpty([], [], 0)
nnode = NeuronNode(leafNeuronNode, leafNeuronNode, False)
brain.seed.node = nnode
list(brain.seed.outSynapses)[0].node = SynapseNode(leafSynapseNode, leafSynapseNode, False)

brain.elapseTime(1.)