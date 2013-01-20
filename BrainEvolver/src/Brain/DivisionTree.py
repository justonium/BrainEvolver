'''
Created on Dec 30, 2012

@author: Justin
'''

from numpy import *
import Neurons
import Synapses
from MutationTools import *

defaultMutationRate = 0.1

class DivisionTree(object):
  
  def __init__(self, root, dataMutationRates, transformMutationRates):
    self.root = root
    self.dataMutationRates = dataMutationRates
    self.transformMutationRates = transformMutationRates
  
  def mutateData(self, data):
    return mutateArray(data, *self.dataMutationRates)
  
  def mutateTransform(self, transform):
    return mutateArray(transform, *self.tranformMutations)
  
  def spawn(self, root):
    return DivisionTree(root, mutateRates(self.dataMutationRates), \
                        mutateRates(self.transformMutationRates))

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
  
  def _spawn(self):
    "This should involve mutations to node fields."
    child = self.copy()
    "This should have a chance of adding a new node."
    child.left = self.left._spawn() if child.left != None else None
    child.right = self.right._spawn() if child.right != None else None
  
  def copy(self):
    raise NotImplementedError


class NeuronNode(DivisionNode):
  
  def __init__(self, left, right, complete, leftTransform=None, rightTransform=None):
    super(NeuronNode, self).__init__(left, right, complete)
    self.leftTransform = leftTransform
    self.rightTransform = rightTransform
  
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


