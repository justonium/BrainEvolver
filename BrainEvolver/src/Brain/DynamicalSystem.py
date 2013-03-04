'''
Created on Jan 30, 2013

@author: Justin
'''

from Tools import *

class DynamicalSystem(object):
  
  def __init__(self, dim, params, data):
    self.dim = dim
    self.params = params
    self.variables = data
  
  def step(self, time):
    raise NotImplementedError
  
  def feedInput(self, input):
    raise NotImplementedError

class CTRNN(DynamicalSystem):
  
  def __init__(self, dataDim, data, inputDim=0):
    if (len(data) != dataDim):
      raise ValueError
    self.dataDim = dataDim
    self.inputDim = inputDim
    self.dim = dataDim + inputDim
    self.z = data
    self.y = sigmoid(self.z)
  
  def reshapeParams(self, params):
    Wsize = self.dataDim*(self.dim + 1)
    alphaSize = self.dataDim
    if (len(params) != Wsize + alphaSize):
      raise ValueError
    return (params[:Wsize].reshape([self.dataDim, self.dim + 1]), params[Wsize:])
  
  def step(self, params, inputs=array([]), time=1.0):
    assert inputs is None or len(inputs) == self.inputDim
    if (inputs is None):
      inputs = array([])
    W = params[0]
    alpha = params[1]
    z_prime = dot(W, concatenate([inputs, self.y, array([1])])) - self.z
    self.z += alpha * z_prime * time
    self.y = sigmoid(self.z)
  
  def feedInput(self, inputs):
    assert len(inputs) <= self.dataDim
    self.z[:len(inputs)] += inputs
    self.y = sigmoid(self.z)

class LDS(DynamicalSystem):
  
  def __init__(self, dataDim, data, inputDim=0):
    if (len(data) != dataDim):
      raise ValueError
    self.dataDim = dataDim
    self.inputDim = inputDim
    self.dim = dataDim + inputDim
    self.y = data
  
  def reshapeParams(self, params):
    Wsize = self.dataDim*(self.dim + 1)
    if (len(params) != Wsize):
      raise ValueError
    return params.reshape([self.dataDim, self.dim + 1])
  
  def step(self, params, inputs=None, time=1.0):
    if (not(inputs is None or len(inputs) == self.inputDim)):
      raise ValueError
    if (inputs is None):
      inputs = array([])
    x_prime = dot(params, concatenate([inputs, self.y, [1]]))
    self.y += x_prime * time
  
  def feedInput(self, inputs):
    assert len(inputs) <= self.dataDim
    self.y[:len(inputs)] += inputs

def getDataSize(T, dim):
  if (T == CTRNN):
    sizes = dim
  elif (T == LDS):
    sizes = dim
  return sizes

def getParamSize(T, dataDim, inputDim=0):
  dim = dataDim + inputDim
  if (T == CTRNN):
    sizes = dataDim*(dim + 1) + dataDim
  elif (T == LDS):
    sizes = dataDim*(dim + 1)
  return sizes




