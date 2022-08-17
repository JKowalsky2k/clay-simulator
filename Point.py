from ast import Constant
import pygame
import math
import Constants

class Point():
    def __init__(self, position, radius, color):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color
        self.center_offset = pygame.math.Vector2(self.radius, self.radius)
        self.bounding_box = pygame.Rect(self.position-self.center_offset, (2*self.radius, 2*self.radius))

    def __updateBBox(self):
        self.bounding_box = pygame.Rect(self.position-self.center_offset, (2*self.radius, 2*self.radius))
    
    def setPosition(self, new_position):
        if new_position[0] - Constants.CLAY_RADIUS < 0:
            self.position.x = Constants.CLAY_RADIUS
        elif new_position[0] + Constants.CLAY_RADIUS > Constants.SCREEN_WIDTH:
            self.position.x = Constants.SCREEN_WIDTH - Constants.CLAY_RADIUS
        else:
            self.position.x = new_position[0]
        
        if new_position[1] - Constants.CLAY_RADIUS < 0:
            self.position.y = Constants.CLAY_RADIUS
        elif new_position[1] + Constants.CLAY_RADIUS > Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT:
            self.position.y = Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT - Constants.CLAY_RADIUS
        else:
            self.position.y = new_position[1]

        self.__updateBBox()

    def setRadius(self, new_radius):
        self.radius = new_radius
        self.__updateBBox()

    def getPosition(self):
        return self.position

    def getBoundingBox(self):
        return self.bounding_box

    def getRadius(self):
        return self.radius
    
    def draw(self, surface):
        pygame.draw.circle(surface=surface, color=self.color, center=self.position, radius=self.radius)
    
    def drawBBox(self, surface):
        pygame.draw.rect(surface=surface, color=Constants.GREEN, rect=self.bounding_box)

