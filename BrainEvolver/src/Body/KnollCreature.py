'''
Created on Jan 22, 2013

@author: Nathan
'''

from Creature import Creature
from GradientSniffer import GradientSniffer
from ArrayInterface import ArrayInterface
from Brain import createEmpty

class KnollCreature(Creature):
    '''
        A simple creature that roams the knolls of the smooth, peaked, gradient map.
        Has only 2 types of senses, and 4 sense total.
    '''

    def __init__(self, x=0, y=0, theta=0):
        '''
        Constructor
        '''
        Creature.__init__(self, x, y, theta)
        
        self.gradL = GradientSniffer(self, self.world, -10)
        self.senses.append((self.gradL))
        
        self.gradC = GradientSniffer(self, self.world, 0)
        self.senses = self.senses.append(self.gradC) 
        
        self.gradR = GradientSniffer(self, self.world, 10)
        self.senses.append(self.gradR)
        
        self.brain_data = ArrayInterface([('gradR', 1), ('gradC', 1), ('gradL', 1)])
        self.brain = createEmpty(range(4), range(4))
        
        