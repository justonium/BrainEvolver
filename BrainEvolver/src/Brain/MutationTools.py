'''
Created on Jan 19, 2013

@author: Justin
'''

from numpy import *

def mutateValue(number, driftRate, zeroRate, nonzeroRate):
  if (number == 0):
    if (random.random() < nonzeroRate):
      number = random.normal()
  else:
    "This is non-symmetric, but probably negligible."
    if (random.random() < zeroRate):
      number = 0
    elif (random.random() < driftRate):
      number *= random.lognormal()
  return number

_mutateArrayFun = vectorize(mutateValue)

def mutateArray(array, driftRates, zeroRates, nonzeroRates):
  return _mutateArrayFun(array, driftRates, zeroRates, nonzeroRates)    



def mutateRate(rate):
  return rate * random.lognormal(sigma=0.1)

_mutateRatesFun = vectorize(mutateRate)

def mutateRates(rates):
  return _mutateRatesFun(rates)






