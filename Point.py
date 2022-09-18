import pygame
import os
import copy
import Constants

class Point(pygame.sprite.Sprite):
    def __init__(self, position, radius, color, trajectory, sprite_texture="clay3.png"):
        pygame.sprite.Sprite.__init__(self)
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color
        self.trajectory = trajectory
        self.center_offset = pygame.math.Vector2(self.radius, self.radius)
        self.sprite_center_offset = pygame.math.Vector2(self.radius, self.radius)
        self.movable = False
        self.bounding_box = pygame.Rect(self.position-self.center_offset, (2*self.radius, 2*self.radius))
        try:
            self.default_sprite = pygame.image.load(os.path.join("images", sprite_texture)).convert_alpha()
            self.sprite = copy.copy(self.default_sprite)
            self.sprite = pygame.transform.scale(self.default_sprite, (2*self.radius, 2*self.radius))
        except Exception as error:
            print(f"Image texture not find ({error})")

    def _updateBBox(self):
        self.bounding_box = pygame.Rect(self.position-self.center_offset, (2*self.radius, 2*self.radius))

    def _updateSprite(self):
        self.sprite_center_offset = pygame.math.Vector2(2*self.radius, 2*self.radius)
        self.sprite = pygame.transform.scale(self.default_sprite, (2*self.radius, 2*self.radius))
    
    def setPosition(self, new_position):
        self.position = new_position
        self._updateBBox()

    def setRadius(self, new_radius):
        self.radius = new_radius
        self.center_offset = pygame.math.Vector2(self.radius, self.radius)
        self._updateBBox()
        self._updateSprite()
    
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

    def drawSprite(self, surface):
        pygame.Surface.blit(surface, self.sprite, self.position-self.center_offset)

