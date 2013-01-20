'''
Created on Dec 30, 2012

@author: Justin
'''

from numpy import *
import Neurons
import Synapses
from MutationTools import *

defaultMutationRate = 0.1
numSharedRates = 2
numNeuronNodeRates = 0
numSynapseNodeRates = 4

class DivisionTree(object):
  
  def __init__(self, root, dataMutationRates, transformMutationRates, \
               sharedRates=zeros(numSharedRates) , otherRates=None):
    self.root = root
    self.dataMutationRates = dataMutationRates
    self.transformMutationRates = transformMutationRates
    self.sharedRates = sharedRates
    self.otherRates = otherRates
  
  def mutateData(self, data):
    return mutateArray(data, *self.dataMutationRates)
  
  def mutateTransform(self, transform):
    return mutateArray(transform, *self.tranformMutations)
  
  def spawn(self, root):
    return DivisionTree(root, mutateRates(self.dataMutationRates), \
        mutateRates(self.transformMutationRates), mutateRates(self.sharedRates), \
        mutateRates(self.otherRates))

class SynapseTree(DivisionTree):
  
  def __init__(self, root, dataMutationRates, transformMutationRates, \
               otherRates=defaultMutationRate*zeros(numSynapseNodeRates)):
    super(DivisionTree, self).__init__(root, dataMutationRates, transformMutationRates, otherRates)

class NeuronTree(DivisionTree):
  
  def __init__(self, root, dataMutationRates, transformMutationRates, \
               otherRates=defaultMutationRate*zeros(numNeuronNodeRates)):
    super(DivisionTree, self).__init__(root, dataMutationRates, transformMutationRates, otherRates)

def emptyMutationRates(shape):
  rateArray = defaultMutationRate * ones(shape)
  return (rateArray, rateArray, rateArray)


class DivisionNode(object):
  
  def __init__(self, left, right, complete, tree=None):
    self.left = left
    self.right = right
    self.complete = complete
  
  "Should only be called on a root."
  def spawn(self):
    child = self._spawn()
    tree = self.tree.spawn(child)
    child.tree = tree
    return child
  
  def _spawn(self, tree):
    child = self.copy()
    "Mutate all the shared fields of this node."
    child.leftTransform = mutateArray(child.leftTransform, tree.transformMutationRates)
    child.rightTransform = mutateArray(child.rightTransform, tree.transformMutationRates)
    
    if (child.complete):
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


class NeuronNode(DivisionNode):
  
  def __init__(self, left, right, complete, leftTransform=None, rightTransform=None):
    super(NeuronNode, self).__init__(left, right, complete)
    self.leftTransform = leftTransform
    self.rightTransform = rightTransform
  
  def _spawn(self, tree):
    child = super(DivisionNode, self).spawn(tree)
    pass
    return child
  
  def copy(self):
    return NeuronNode(self.left, self.right, self.complete, self.leftTransform, self.rightTransform)


class SynapseNode(DivisionNode):
  
  def __init__(self, left, right, complete, sourceCarries=[], sinkCarries=[], symmetric=False, \
               leftTransform=None, rightTransform=None):
    super(SynapseNode, self).__init__(left, right, complete)
    self.sourceCarries = sourceCarries
    self.sinkCarries = sinkCarries
    self.symmetric = symmetric
    self.leftTransform = leftTransform
    self.rightTransform = rightTransform
  
  def _spawn(self, tree):
    child = super(DivisionNode, self).spawn(tree)
    
    if (random.random() < tree.otherRates[0]):
      child.sourceCarries.append(0)
    
    if (random.random() < tree.otherRates[1]):
      child.sourceCarries.append(1)
    
    if (random.random() < tree.otherRates[2]):
      child.sinkCarries.append(0)
    
    if (random.random() < tree.otherRates[3]):
      child.sinkCarries.append(1)
    
    if (random.random() < tree.otherRates[4]):
      child.sourceCarries.remove(0)
    
    if (random.random() < tree.otherRates[5]):
      child.sinkCarries.remove(0)
    
    if (random.random() < tree.otherRates[6]):
      index = random.random_integers(len(child.sourceCarries) - 1)
      child.sourceCarries.remove(index)
    
    if (random.random() < tree.otherRates[7]):
      index = random.random_integers(len(child.sinkCarries) - 1)
      child.sinkCarries.remove(index)
    
    if (random.random() < tree.otherRates[8]):
      index = random.random_integers(len(child.sourceCarries) - 1)
      child.sourceCarries = child.sourceCarries[-(index + 1):]
    
    if (random.random() < tree.otherRates[9]):
      index = random.random_integers(len(child.sinkCarries) - 1)
      child.sinkCarries = child.sinkCarries[-(index + 1):]
    
    "do stuff with symmetric"
    if (random.random() < tree.otherRates[10]):
      pass
    
    if (random.random() < tree.otherRates[11]):
      pass
    
    return child
  
  def copy(self):
    return SynapseNode(self.left, self.right, self.complete, self.sourceCarries, self.sinkCarries, \
                       self.symmetric, self.leftTransform, self.rightTransform)
  
  def isReady(self):
    return not (self.sourceCarries and not self.source.node.complete) \
      and not (self.sinkCarries and not self.sink.node.complete)

leafNeuronNode = NeuronNode(None, None, True)

leafSynapseNode = SynapseNode(None, None, True)

def rootNeuronNode():
  node = NeuronNode(None, None, True)
  node.tree = DivisionTree(node, emptyMutationRates((Neurons.divisionDataSize)), \
      emptyMutationRates((Neurons.divisionTransformWidth, Neurons.divisionTransformWidth + 1)))
  return node

def rootSynapseNode():
  node = SynapseNode(None, None, True)
  node.tree = DivisionTree(node, emptyMutationRates((Synapses.divisionDataSize)), \
      emptyMutationRates((Neurons.divisionTransformWidth, Synapses.divisionTransformWidth + 1)))
  return node


