'''
Created on Dec 30, 2012

@author: Justin
'''

class DivisionTree(object):
  
  def __init__(self):
    self.root


class DivisionNode(object):
  
  def __init__(self, left, right, complete):
    self.left = left
    self.right = right
    self.complete = complete


class NeuronNode(DivisionNode):
  
  def __init__(self, left, right, complete, leftTransform=None, rightTransform=None):
    super(NeuronNode, self).__init__(left, right, complete)
    self.leftTransform = leftTransform
    self.rightTransform = rightTransform


class SynapseNode(DivisionNode):
  
  def __init__(self, left, right, complete, sourceCarries=[], sinkCarries=[], symmetric=False, \
               leftTransform=None, rightTransform=None):
    super(SynapseNode, self).__init__(left, right, complete)
    self.sourceCarries = sourceCarries
    self.sinkCarries = sinkCarries
    self.symmetric = symmetric
    self.leftTransform = leftTransform
    self.rightTransform = rightTransform
  
  def isReady(self):
    return not (self.sourceCarries and not self.source.node.complete) \
      and not (self.sinkCarries and not self.sink.node.complete)



leafNeuronNode = NeuronNode(None, None, True)

leafSynapseNode = SynapseNode(None, None, True)


