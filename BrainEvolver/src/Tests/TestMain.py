'''
Created on Jan 17, 2013

@author: Justin
'''

from numpy import *

prod = 1.0
for i in range(1000):
  prod *= random.lognormal(0)

print prod