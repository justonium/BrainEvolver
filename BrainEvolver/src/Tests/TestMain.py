'''
Created on Jan 17, 2013

@author: Justin
'''

class Foo(object):
  def __init__(self, bar):
    print 'bar' in self.__dict__
    self.bar = bar
    print 'bar' in self.__dict__
    print 'bar2' in self.__dict__

a = Foo('hi')