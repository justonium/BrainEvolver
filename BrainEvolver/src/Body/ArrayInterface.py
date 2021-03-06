'''
Created on Jan 20, 2013

@author: Justin
'''

from numpy import *

'''
This object lets you access and edit arrays in it, and also access the field 'data',
which contains all of the arrays concatenated together.
'''
class ArrayInterface(object):
  
  '''
  Takes a list of pairs, where the first element is the name you would like to use to access an array,
  and the second is the array's size
  '''
  def __init__(self, nameSizePairs):
    self.data = None
    
    self.size = 0
    
    self._accessDict = {}
    self._writeDict = {'dataDim' : deny}
    
    for name, dataDim in nameSizePairs:
      start = self.size
      self._accessDict[name] = lambda start=start, dataDim=dataDim : self.data[start:start + dataDim]
      self._writeDict[name] = self.writeVector(start, start + dataDim)
      self.size += dataDim
    
    self.data = zeros(self.size)
  
  def zero(self):
    self.data = 0*self.data
  
  "The following 3 methods were copied and pasted from Cell."
  def writeVector(self, location, end):
    def _writeVector(self, value):
      self.data[location:end] = value
    return _writeVector
  
  def __setattr__(self, fieldname, value):
    if (fieldname in self.__dict__ or not '_writeDict' in self.__dict__):
      object.__setattr__(self, fieldname, value)
    else:
      self._writeDict[fieldname](self, value)
  
  def __getattr__(self, fieldname):
    return self._accessDict[fieldname]()
 
def deny(arg1, arg2):
  raise Exception('You can''t do that.')


"example code"
'''
interface = ArrayInterface([('vector1', 4), ('vector2', 1)])
interface.vector1 = range(4)
interface.vector2 = [4]
print interface.vector1 #prints range(4)
print interface.data #prints range(5)
'''