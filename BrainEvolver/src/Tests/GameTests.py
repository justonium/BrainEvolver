'''
Created on Jan 20, 2013

@author: Nathan
'''

from World.World import World
from Body.ArrayInterface import ArrayInterface

if __name__ == '__main__':
    #world = World((2000, 2000))
    #world.simulate()
    ai = ArrayInterface([('hai', 10), ('bai', 5)])
    ai.hai = range(10)
    ai.bai = range(5) 
    
    varg = ai.hai