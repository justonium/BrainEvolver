'''
Created on Jan 18, 2013

@author: Nathan
'''
import pygame
from pygame.sprite import Sprite
from pygame import Surface
from random import randrange
from World import SCALE_FLAG
class Floor(Sprite):
    '''
    classdocs
    '''

    def __init__(self, width=640, height=480):
        '''
        Constructor
        '''
        self.width = width
        self.height = height
        self.visionGrid = []
        self.heightMap = [[]]
        self.heightFunction = self._defaultHF
        self.image = pygame.image.load('heightmap.png')
        self.rect = (0, 0, self.width, self.height)
        self.vertices = []
        self.peaks = 300
        
        for _ in xrange(self.peaks):
            self.vertices.append((randrange(self.width), randrange(self.height)))
            
        if not self.image:
            self.image = Surface((self.width, self.height))
            self._render()
        
        pygame.image.save(self.image, 'heightmap.png')
        
        if SCALE_FLAG:
            tmpimg = pygame.transform.scale2x(self.image)
            del self.image
            self.image = tmpimg
        
    
    def _render(self):
        self.image.fill(pygame.Color(255, 255, 255))
        pxArr = pygame.PixelArray(self.image)
        if not self.heightFunction:
            for y in xrange(len(self.heightMap)):
                for x in xrange(len(self.heightMap[0])):
                    pxArr[y][x] = self.heightMap[y][x]
        else:
            for y in xrange(self.height):
                print 'y value: ' + str(y)
                for x in xrange(self.width):
                    c = self.heightFunction(x, y)
                    pxArr[x][y] =  pygame.Color(int(c * 255), int(c * 255), int(c * 255))
                    #pygame.draw.rect(self.image, pygame.Color(int(c * 255), int(c * 255), int(c * 255)), (x, y, 1, 1))
        
        del pxArr
        print 'done rendering' 
    
    def _defaultHF(self, cx, cy):
        mind = 999999
        for vert in self.vertices:
            x = (float(cx) - vert[0]) / 90
            y = (float(cy) - vert[1]) / 90
            
            d = x**2 + y**2
            if d < mind:
                mind = d
        return 1 - (1 / (1 + mind))
        
            