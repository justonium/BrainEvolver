'''
Created on Jan 22, 2013

@author: Nathan
'''
from random import randrange

FOOD_DEFAULT = 1000

class ResourceManager(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        ' dict mapping resource type to list '
        self.resources = dict() 

class FoodNurturer(ResourceManager):
    def __init__(self, world):
        self.world = world
        self.gwidth = self.world.world_size[0]
        self.gheight = self.world.world_size[1]
        self.grid = []
        
        'Create the empty grid'
        for _ in xrange(self.gheight):
            self.grid.append([0] * self.gwidth)
        
        self.__seed()
            
    def __seed(self):
        num_fuds = FOOD_DEFAULT + randrange(int(0.1 * FOOD_DEFAULT))
        xlist = range(self.gwidth)
        ylist = range(self.gheight)
        for _ in range(num_fuds):
            xc = randrange(len(xlist))
            yc = randrange(len(ylist))
            xc = xlist.pop(xc)
            yc = ylist.pop(yc)
            self.grid[yc][xc] = 0xFFFF
    
    def update(self):
        pass
        