'''
Created on Dec 30, 2012

@author: Justin
'''

try:
  from numpypy import *
except:
  from numpy import *
import random
import Synapses
import Neurons
from Neurons import defaultNeuronTransform
from Synapses import defaultSynapseTransform
from MutationTools import *

defaultMutationRate = 0.1
numSharedRates = 2
numNeuronNodeRates = 0
numSynapseNodeRates = 12

class DivisionTree(object):
  
  def __init__(self, root, dataMutationRates, transformMutationRates, \
               otherRates=None, sharedRates=defaultMutationRate*ones(numSharedRates)):
    self.root = root
    self.dataMutationRates = dataMutationRates #tuple
    self.transformMutationRates = transformMutationRates #tuple
    self.sharedRates = sharedRates
    self.otherRates = otherRates
  
  def mutateData(self, data):
    return mutateArray(data, *self.dataMutationRates)
  
  def mutateTransform(self, transform):
    return mutateArray(transform, *self.tranformMutations)
  
  def spawn(self, root):
    dataMutationRates = tuple([mutateRates(vec) for vec in self.dataMutationRates])
    transformMutationRates = tuple([mutateRates(vec) for vec in self.transformMutationRates])
    return DivisionTree(root, dataMutationRates, \
        transformMutationRates, mutateRates(self.otherRates), \
        mutateRates(self.sharedRates))

class NeuronTree(DivisionTree):
  
  def __init__(self, root, dataMutationRates, transformMutationRates, \
               otherRates=defaultMutationRate*ones(numNeuronNodeRates)):
    super(NeuronTree, self).__init__(root, dataMutationRates, transformMutationRates, otherRates)

class SynapseTree(DivisionTree):
  
  def __init__(self, root, dataMutationRates, transformMutationRates, \
               otherRates=defaultMutationRate*ones(numSynapseNodeRates)):
    super(SynapseTree, self).__init__(root, dataMutationRates, transformMutationRates, otherRates)


class DivisionNode(object):
  
  def __init__(self, left, right, complete, leftTransform, rightTransform, tree=None):
    self.left = left
    self.right = right
    self.complete = complete
    self.leftTransform = leftTransform
    self.rightTransform = rightTransform
    self.tree = None
  
  "Should only be called on a root."
  def spawn(self):
    child = self._spawn(self.tree)
    tree = self.tree.spawn(child)
    child.tree = tree
    return child
  
  def _spawn(self, tree):
    child = self.copy()
    "Mutate all the shared fields of this node."
    child.leftTransform = mutateArray(child.leftTransform, *tree.transformMutationRates)
    child.rightTransform = mutateArray(child.rightTransform, *tree.transformMutationRates)
    
    if (self.complete):
      if (random.random() < tree.sharedRates[0]):
        "Become a parent and have 2 leaf children."
        child.complete = False
        child.left = self.getLeafNode()
        child.right = self.getLeafNode()
        
    else:
      if (random.random() < tree.sharedRates[1]):
        "Delete children and become a leaf."
        child.left = None
        child.right = None
        child.complete = True
      child.left = self.left._spawn(tree)
      child.right = self.right._spawn(tree)
    
    return child
  
  def copy(self):
    raise NotImplementedError
  
  def getLeafNode(self):
    if (type(self) == NeuronNode):
      return leafNeuronNode
    elif (type(self) == SynapseNode):
      return leafSynapseNode
  
  def treeSize(self):
    return 1 if self.complete else self.left.treeSize() + self.right.treeSize()


class NeuronNode(DivisionNode):
  
  def __init__(self, left, right, complete, leftTransform, rightTransform):
    super(NeuronNode, self).__init__(left, right, complete, leftTransform, rightTransform)
  
  def _spawn(self, tree):
    child = super(NeuronNode, self)._spawn(tree)
    pass
    return child
  
  def copy(self):
    return NeuronNode(self.left, self.right, self.complete, self.leftTransform, self.rightTransform)


class SynapseNode(DivisionNode):
  
  def __init__(self, left, right, complete, leftTransform, rightTransform, \
               sourceCarries=[], sinkCarries=[], symmetric=False):
    super(SynapseNode, self).__init__(left, right, complete, leftTransform, rightTransform)
    self.sourceCarries = sourceCarries
    self.sinkCarries = sinkCarries
    self.symmetric = symmetric
  
  def _spawn(self, tree):
    child = super(SynapseNode, self)._spawn(tree)
    
    if (random.random() < tree.otherRates[0]):
      child.sourceCarries.append(0)
    
    if (random.random() < tree.otherRates[1]):
      child.sourceCarries.append(1)
    
    if (random.random() < tree.otherRates[2]):
      child.sinkCarries.append(0)
    
    if (random.random() < tree.otherRates[3]):
      child.sinkCarries.append(1)
    
    if (self.sourceCarries):
      
      if (random.random() < tree.otherRates[4]):
        del child.sourceCarries[0]
      
      elif (random.random() < tree.otherRates[5]):
        index = random.randint(0, len(child.sourceCarries) - 1)
        del child.sourceCarries[index]
      
      elif (random.random() < tree.otherRates[6]):
        index = random.randint(0, len(child.sourceCarries) - 1)
        child.sourceCarries = child.sourceCarries[-(index + 1):]
    
    if (self.sinkCarries):
      
      if (random.random() < tree.otherRates[7]):
        del child.sinkCarries[0]
      
      elif (random.random() < tree.otherRates[8]):
        index = random.randint(0, len(child.sinkCarries) - 1)
        del child.sinkCarries[index]
      
      elif (random.random() < tree.otherRates[9]):
        index = random.randint(0, len(child.sinkCarries) - 1)
        child.sinkCarries = child.sinkCarries[-(index + 1):]
    
    "do stuff with symmetric"
    if (self.symmetric):
      if (random.random() < tree.otherRates[10]):
        child.setSymmetric(False)
    else:
      if (random.random() < tree.otherRates[11]):
        child.setSymmetric(True)
    
    return child
  
  def setSymmetric(self, symmetric):
    self.symmetric = symmetric
    if (not self.complete):
      self.left.setSymmetric(symmetric)
      self.right.setSymmetric(symmetric)
  
  def copy(self):
    return SynapseNode(self.left, self.right, self.complete, self.leftTransform, self.rightTransform, \
                       self.sourceCarries, self.sinkCarries, self.symmetric)

leafNeuronNode = NeuronNode(None, None, True, defaultNeuronTransform(), defaultNeuronTransform())

leafSynapseNode = SynapseNode(None, None, True, defaultSynapseTransform(), defaultSynapseTransform())

def rootNeuronNode():
  node = NeuronNode(None, None, True, defaultNeuronTransform(), defaultNeuronTransform())
  node.tree = SynapseTree(node, emptyMutationRates((Neurons.divisionDataSize)), \
      emptyMutationRates((2, Neurons.divisionDataSize)))
  return node

def rootSynapseNode():###symmetric shouldn't be True
  node = SynapseNode(None, None, True, defaultSynapseTransform(), defaultSynapseTransform())
  node.tree = SynapseTree(node, emptyMutationRates((Synapses.divisionDataSize)), \
      emptyMutationRates((2, Synapses.divisionDataSize)))
  return node





