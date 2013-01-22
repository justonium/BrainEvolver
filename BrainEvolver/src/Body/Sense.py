'''
Created on Jan 21, 2013

@author: Nathan
'''

sense_history = 2

class Sense(object):
    def __init__(self, world):
        ''' the actually data that the sense contains '''
        self.repData = [None] * sense_history
        
        ''' the world instance that this sense reads from
            TODO: consider making an interface to the world
        '''
        self.world = world
        
        ''' Relative positions to the creature/body '''
        self.rel_x = 0
        self.rel_y = 0
    
    def tick(self):
        self.__gather(self.worlds)
    
    def __gather(self, world):
        raise NotImplementedError('__gather is not defined in base class Sense')