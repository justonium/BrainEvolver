'''
Created on Jan 15, 2013

@author: Justin
'''

from numpy import *

def createIdentityTransform(dataSize):
  return zeros(dataSize, dataSize + 1)
  #return hstack(zeros(dataSize, 1), identity(dataSize))

def applyTransform(data, transform):
  if (data == None):
    pass
  if (transform == None):
    pass
  return dot(transform, append(array(1), data))

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



maxRate = 24. #the frame rate of most movies
minDelay = 1/maxRate

def sampleDelay(rate):
  return minDelay + random.exponential(1/rate) if rate > 0 else inf



#this can be co-optimized with the call to exp so that only 1 exp is called.
def sigmoid(z):
  return 1.0/(1.0 + exp(-z))

def rectLinear(z):
  return 0.0 if z < 0 else z

def smoothRectLinear(z):
  return log(1.0 + exp(z))





