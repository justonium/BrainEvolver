'''
Created on Jan 22, 2013

@author: Nathan
'''

from pygame.sprite import Sprite
CODE_VALID = 'notAbstract'
class WorldObject(Sprite):
    '''
    classdocs
    '''

    def __init__(self, code='invalid'):
        '''
        Constructor
        '''
        if code != CODE_VALID:
            raise Exception('WorldObject is abstract. Please do not instantiate.')
        self.x = None
        self.y = None
        
        
    
    def _render(self):
        raise NotImplementedError('The base class WorldObject has nothing to render.')