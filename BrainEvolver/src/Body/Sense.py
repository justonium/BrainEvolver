'''
Created on Jan 21, 2013

@author: Nathan
'''

''' Future ability to have a bit of short-term sensual memory '''
sense_history = 1

class Sense(object):
    def __init__(self, creature, world):
        ''' the actually data that the sense contains '''
        self.repData = [None] * sense_history
        
        '''
            Self explanatory
        '''
        self.creature = creature
        
        ''' the world instance that this sense reads from
            TODO: consider making an interface to the world
        '''
        self.world = world
        
        ''' Relative positions to the creature/body '''
        self.rel_x = 0
        self.rel_y = 0
        
        self.llname = "base_sense"
    
    def tick(self):
        self.__gather(self.worlds)
    
    def __gather(self, world):
        raise NotImplementedError('__gather is not defined in base class Sense')
    
    ''' TODO: UPDATE '''
    def __push(self, datum):
        self.repData[0] = datum