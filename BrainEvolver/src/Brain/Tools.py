'''
Created on Jan 15, 2013

@author: Justin
'''

from numpy import *

def createIdentity(dataSize):
  return hstack(zeros(dataSize, 1), identity(dataSize))

def applyTransform(data, transform):
  return dot(transform, append(array(1), data))

def transformSize(x):
  return x * (x + 1)

def reduceSize(x):
  return x + 1

def rollTransform(vector, width):
  return reshape(vector, [width, width + 1])



maxRate = 24. #the frame rate of most movies
minDelay = 1/maxRate

def sampleDelay(rate):
  return minDelay + random.exponential(1/rate)



#this can be co-optimized with the call to exp so that only 1 exp is called.
def sigmoid(z):
  return 1.0/(1.0 + exp(-z))

def rectLinear(z):
  return 0.0 if z < 0 else z

def smoothRectLinear(z):
  return log(1.0 + exp(z))