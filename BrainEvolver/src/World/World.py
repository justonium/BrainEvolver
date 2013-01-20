'''
Created on Jan 18, 2013

@author: Nathan
'''
import pygame, sys
from pygame.locals import *
from Floor import Floor
from Body.Creature import Creature
from random import randrange

num_creatures = 3

class World(object):
    '''
        Forms the basis of the game world.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.display_size = (800, 600)
        self.fpsClock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption('Initial Test')
        self.mousex, self.mousey = 0, 0
        self.floor = Floor(self.display_size[0], self.display_size[1])
        self.creatures = []
        
        for no in xrange(num_creatures):
            self.creatures.append(Creature(randrange(self.display_size[0]), randrange(self.display_size[1]), randrange(360)))

    def simulate(self):
        while True:
            self.__tick()
            pygame.display.update()
            self.fpsClock.tick(30) # 30 fps
    
    def __tick(self):
        self.window.blit(self.floor.image, (0, 0))
        
        for creat in self.creatures:
            self.window.blit(creat.image, (creat.x, creat.y))
            creat.tick()
        self.__checkEvents()
        
        
    def __checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()