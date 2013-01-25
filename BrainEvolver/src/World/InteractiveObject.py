'''
Created on Jan 22, 2013

@author: Nathan
'''

from WorldObject import WorldObject
from WorldObject import CODE_VALID

class InteractiveObject(WorldObject):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        WorldObject.__init__(CODE_VALID)
        
    