'''
Created on Jan 15, 2013

@author: Justin
'''

from Brain import *

synapse = Synapse(None, None, leafSynapseNode)
nnode = NeuronNode(leafNeuronNode, leafNeuronNode, False)
seed = Neuron(leafNeuronNode, set(), set())
brain = Brain(seed, set(), set(), 0)

#brain2 = brain.spawn()