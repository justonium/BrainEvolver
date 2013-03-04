'''
Created on Jan 15, 2013

@author: Justin
'''

try:
  from numpypy import *
except:
  from numpy import *
import random

def createIdentityTransform(dataSize):
  return zeros(dataSize, dataSize + 1)
  #return hstack(zeros(dataSize, 1), identity(dataSize))

def applyTransform(data, transform):
  if (data is None):
    pass
  if (transform is None):
    pass
  
  return dot(transform, concatenate((data, [1])))

def createIdentityMap(dataSize):
  return zeros((2, dataSize))

def applyMap(data, transform):
  return dot(transform[0,:], data) + transform[1,:]

def transformSize(width, height=None):
  if (height == None):
    height = width
  return height * (width + 1)

def reduceSize(x):
  return x + 1

def rollTransform(vector, width, height=None):
  if (height == None):
    height = width
  return reshape(vector, [height, width + 1])



maxRate = 12.0
minDelay = 1/maxRate

def sampleDelay(rate):
  if (rate == inf):
    delay = minDelay
  elif (rate > 0):
    delay = minDelay + random.expovariate(rate)
  else:
    delay = inf
  return delay



#this can be co-optimized with the call to exp so that only 1 exp is called.
def sigmoid(z):
  return 1.0/(1.0 + exp(-z))

def rectLinear(z):
  return 0.0 if z < 0 else z

def smoothRectLinear(z):
  return log(1.0 + exp(z))



def concatenate2(arrays):
  length = 0
  for array in arrays:
    length += len(array)
  result = zeros(length)
  
  i = 0
  for array in arrays:
    length = len(array)
    result[i:i+length] = array
    i = i + length
  
  return result


