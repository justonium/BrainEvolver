'''
Created on Jan 15, 2013

@author: Justin
'''

class A(object):
  def __init__(self):
    self.a = 0

o = A()
t = A
print t
print type(o)
o2 = type(o)()
print type(o) == A