'''
Created on Dec 30, 2012

@author: Nathan
'''
import pygame
import random
import math
from pygame.sprite import Sprite
from pygame import Surface
from numpy.random import randn
from random import randrange
from math import sqrt
from Brain.Brain import createEmpty

CREATURE_WIDTH = 25
CREATURE_HEIGHT = 25

def deg2rad(angle):
    return math.pi * angle / 180

class Creature(Sprite):
    '''
        Class represents a 
    '''
    def __init__(self, x=0, y=0, theta=0):
        self.y = x
        self.y = y
        self.theta = theta
        self.v = 1
        self.energy = 5000 + abs(50 * randn())
        self.brain = createEmpty(10, 10)
        self.width = CREATURE_WIDTH
        self.height = CREATURE_HEIGHT
        
        self.senses = []
        
        self.base_image = Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.base_image = self.base_image.convert_alpha()
        
        self.brain_data = None
        
        self.rect = (0, 0, self.width, self.height)
        self._render()
        self.image = pygame.transform.rotate(self.base_image, theta)
        
    ''' updates the creature for the next round '''
    def tick(self):
        self.brain.elapseTime(10, [(randrange(1, 1000) * 1.0)/ 1000 for _ in xrange(10)])
        self.y -= math.sin(deg2rad(self.theta)) * self.v
        self.y += math.cos(deg2rad(self.theta)) * self.v 
        self.theta += (random.randrange(60)) - 30
        self.image = pygame.transform.rotate(self.base_image, self.theta)
        
    ''' rendering for the basic, ugly creature '''
    def _render(self):
        pygame.draw.circle(self.base_image, pygame.Color(0, 128, 64), (self.width/2, self.height/2), self.width/2, self.width/2)
        s = sqrt(2) * 12
        pygame.draw.rect(self.base_image, pygame.Color(0, 128, 64), (round(12.5 - s/2), round(12.5 - s/2), s, s))
        pygame.draw.line(self.base_image, pygame.Color(255, 10, 10), (12, 12), (24, 12), 1)
