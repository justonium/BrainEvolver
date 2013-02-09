'''
Created on Jan 15, 2013

@author: Justin
'''

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

o = A()
o.data = 'hi'
print o.data




