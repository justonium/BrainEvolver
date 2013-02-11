'''
Created on Jan 21, 2013

@author: Nathan
'''
from Sense import Sense

class GradientSniffer(Sense):
    '''
    classdocs
    '''
    def __init__(self, creature, world, x_offset=0):
        '''
        Constructor
        '''
        Sense.__init__(creature, world)
        
        ''' Relative positions to the creature/body '''
        self.rel_x = 0
        self.rel_y = -20
        
        self.llname = "grad_sense"
    
    def __gather(self, world):
        val = world.getFloorPixel(self.creature.y + self.rel_x, self.creature.y + self.rel_y)
        self.__push(val)
        