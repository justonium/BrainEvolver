'''
Created on Jan 15, 2013

@author: Justin
'''

class Test(object):
  def __init__(self):
    self.value = 0
  def f(self, value):
    self.value = value
  def g(self):
    return self.f

t = Test()
f = t.g()
f(1)
print t.value