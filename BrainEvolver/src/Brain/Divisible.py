'''
Created on Dec 30, 2012

@author: Justin
'''

class Divisible(object):
  
  def __init__(self):
    self.accessDict = None
    self.writeDict = None
  
  def divide(self):
    raise NotImplementedError
  
  def finalize(self):
    raise NotImplementedError
  
  def writeValue(self, location):
    def _writeValue(self, value):
      self.data[location] = value
    _writeValue
  
  def writeVector(self, location, end):
    def _writeVector(self, value):
      self.data[location:end] = value
    _writeVector
  
  def __setattr__(self, fieldname, value):
    if (not self.__dict__.has_key(fieldname) or fieldname in self.__dict__):
      object.__setattr__(self, fieldname, value)
    else:
      self.writeDict[fieldname](value)
  
  def __getattr__(self, fieldname, value):
    self.accessDict[fieldname](value)