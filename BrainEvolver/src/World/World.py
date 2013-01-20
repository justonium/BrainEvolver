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
        For now it contains the pygame window code too. I don't like this
        so this will change.
    '''

    def __init__(self, world_size):
        '''
        Constructor
        '''
        self.display_size = (1024, 768)
        self.world_size = tuple(world_size)
        self.fpsClock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption('Initial Test')
        self.mousex, self.mousey = 0, 0
        self.floor = Floor(self.world_size[0], self.world_size[1])
        self.creatures = []
        self.floor_pos = (0, 0)
        self.lastClick = (0, 0)
        
        for no in xrange(num_creatures):
            self.creatures.append(Creature(randrange(self.display_size[0]), randrange(self.display_size[1]), randrange(360)))

    def simulate(self):
        while True:
            self.__tick()
            pygame.display.update()
            self.fpsClock.tick(30) # 30 fps
    
    def _t(self, coords):
        return (coords[0] + self.floor_pos[0], coords[1] + self.floor_pos[1])
    
    def _it(self, coords):
        return (coords[0] - self.floor_pos[0], coords[1] - self.floor_pos[1])
    
    def __tick(self):
        pygame.draw.rect(self.window, pygame.Color(40, 40, 40), (0, 0, self.display_size[0], self.display_size[1]))
        self.window.blit(self.floor.image, self.floor_pos)
        
        for creat in self.creatures:
            self.window.blit(creat.image, self._t((creat.x, creat.y)))
            creat.tick()
            if creat.x < 0:
                creat.x = 0
                
            if creat.y < 0:
                creat.y = 0
                
        self.__checkEvents()
        
        
    def __checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if 1 == event.button:
                    self.lastClick = tuple(event.pos)
                    self.floor_poso = self.floor_pos
            elif event.type == MOUSEMOTION:
                if 1 in event.buttons:
                    self.floor_pos = (self.floor_poso[0] + event.pos[0] - self.lastClick[0], self.floor_poso[1] + event.pos[1] - self.lastClick[1]) 
                