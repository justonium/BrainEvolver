'''
Created on Jan 19, 2013

@author: Justin
'''

try:
  from numpypy import *
except:
  from numpy import *
import random
import DivisionTree

def mutateValue(number, driftRate, zeroRate, nonzeroRate):
  if (number == 0):
    if (random.random() < nonzeroRate):
      number = random.gauss(0, 0.2)
  else:
    "This is non-symmetric, but probably negligible."
    if (random.random() < zeroRate):
      number = 0
    elif (random.random() < driftRate):
      number *= random.lognormvariate(0, 0.5)
  return number

'''
_mutateArrayFun = vectorize(mutateValue)

def mutateArray(array, driftRates, zeroRates, nonzeroRates):
  return _mutateArrayFun(array, driftRates, zeroRates, nonzeroRates)
'''
"This is slow and un-vectorized."
def mutateArray(array, driftRates, zeroRates, nonzeroRates):
  shape = array.shape
  result = zeros(shape)
  d = len(shape)
  if (d == 1):
    for i in range(shape[0]):
      result[i] = mutateValue(array[i], driftRates[i], zeroRates[i], nonzeroRates[i])
  elif (d == 2):
    for i in range(shape[0]):
      for j in range(shape[1]):
        result[i,j] = mutateValue(array[i,j], driftRates[i,j], zeroRates[i,j], nonzeroRates[i,j])
  else:
    raise NotImplementedError
  return result


def mutateRate(rate):
  return rate * random.lognormvariate(0, 0.1)

'''
_mutateRatesFun = vectorize(mutateRate)

def mutateRates(rates):
  return _mutateRatesFun(rates)
'''
"This is slow and un-vectorized."

def mutateRates(rates):
  shape = rates.shape
  result = zeros(shape)
  d = len(shape)
  if (d == 1):
    for i in range(shape[0]):
      result[i] = mutateRate(rates[i])
  elif (d == 2):
    for i in range(shape[0]):
      for j in range(shape[1]):
        result[i,j] = mutateRate(rates[i,j])
  else:
    raise NotImplementedError
  return result


def emptyMutationRates(shape):
  rateArray = DivisionTree.defaultMutationRate * ones(shape)
  return (rateArray, rateArray, rateArray)






