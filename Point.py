import pygame
import Constants

class Point():
    def __init__(self, position, radius, color, trajectory):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color
        self.trajectory = trajectory
        self.center_offset = pygame.math.Vector2(self.radius, self.radius)
        self.movable = False
        self.bounding_box = pygame.Rect(self.position-self.center_offset, (2*self.radius, 2*self.radius))

    def _updateBBox(self):
        self.bounding_box = pygame.Rect(self.position-self.center_offset, (2*self.radius, 2*self.radius))
    
    def setPosition(self, new_position):
        self.position = new_position
        self._updateBBox()

    def setRadius(self, new_radius):
        self.radius = new_radius
        self._updateBBox()
    
    def setMovable(self, state: bool):
        self.movable = state

    def getPosition(self):
        return self.position

    def getBoundingBox(self):
        return self.bounding_box

    def getRadius(self):
        return self.radius
    
    def isMovable(self):
        return self.movable
    
    def draw(self, surface):
        pygame.draw.circle(surface=surface, color=self.color, center=self.position, radius=self.radius)
    
    def drawBBox(self, surface):
        pygame.draw.rect(surface=surface, color=Constants.GREEN, rect=self.bounding_box)

