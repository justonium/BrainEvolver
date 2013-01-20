'''
Created on Dec 30, 2012

@author: Justin
'''

from heapq import *

class Cell(object):
  
  def __init__(self):
    self.accessDict = None
    self.writeDict = None
    self.nextEvent = None
  
  def divide(self):
    raise NotImplementedError
  
  def finalize(self):
    raise NotImplementedError
  
  def spawn(self):
    raise NotImplementedError
  
  def pushEvent(self, action, executionTime):
    event = Event(self, action, executionTime)
    self.nextEvent = event
    heappush(self.brain.events, event)
  
  def writeValue(self, location):
    def _writeValue(self, value):
      self.data[location] = value
    return _writeValue
  
  def writeVector(self, location, end):
    def _writeVector(self, value):
      self.data[location:end] = value
    return _writeVector
  
  def __setattr__(self, fieldname, value):
    if (not self.__dict__.has_key(fieldname) or fieldname in self.__dict__):
      object.__setattr__(self, fieldname, value)
    else:
      self.writeDict[fieldname](value)
  
  def __getattr__(self, fieldname):
    return self.accessDict[fieldname]()



class Event(object):
  
  def __init__(self, neuron, action, executionTime):
    self.neuron = neuron
    self.action = action
    self.executionTime = executionTime
    self.active = True
  
  def execute(self):
    self.action()