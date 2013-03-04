'''
Created on Jan 15, 2013

@author: Justin
'''

try:
  from numpypy import *
except:
  from numpy import *
from Brain.Tools import concatenate

class A(object):
  def __init__(self):
    pass
  def _get_data(self):
    return self.__data
  def _set_data(self, data):
    if not isinstance(data, int):
      raise TypeError("data must be set to an integer")
    self.__data = data
  data = property(_get_data, _set_data)

#print concatenate([array([1,2]), array([3]), array([4,5])])
for i in range(10):
  i +=2
  print i


