'''
Created on Jan 18, 2013

@author: Nathan
'''
import pygame, sys
from pygame.locals import *

class World(object):
    '''
        Forms the basis of the game world.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.fpsClock = pygame.time.Clock()
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Initial Test')
        self.mousex, self.mousey = 0, 0
        
        while True:
            self.tick()
            pygame.display.update()
            self.fpsClock.tick(30) # 30 fps
            

    def tick(self):
        pygame.draw.circle(self.window, pygame.Color(225, 0, 45), (300, 50), 20, 20)
        pygame.draw.circle(self.window, pygame.Color(225, 0, 45), (300, 50), 20, 20)
        pygame.draw.circle(self.window, pygame.Color(225, 0, 45), (300, 50), 20, 20)
        #arr = pygame.PixelArray(self.window)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()