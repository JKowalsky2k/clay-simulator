import pygame
import copy
import os
import Constants

class House(pygame.sprite.Sprite):
    def __init__(self, position, width, height, color, trajectory, sprite_texture="clay3.png") -> None:
        pygame.sprite.Sprite.__init__(self)
        self.position = pygame.math.Vector2(position)
        self.width = width
        self.height = height
        self.color = color
        self.trajectory = trajectory
        self.center_offset = pygame.math.Vector2(self.width // 2, self.height // 2)
        self.movable = False
        self.bounding_box = pygame.Rect(self.position, (self.width, self.height))
        self._updateBBox()
        try:
            self.default_sprite = pygame.image.load(os.path.join("images", sprite_texture)).convert_alpha()
            self.sprite = copy.copy(self.default_sprite)
            self.sprite = pygame.transform.scale(self.default_sprite, (self.width, self.height))
        except Exception as error:
            print(f"Image texture not find ({error})")

    def _updateBBox(self):
        self.bounding_box = pygame.Rect(self.position, (self.width, self.height))
        self.bounding_box.center = self.position

    def _updateSprite(self):
        self.sprite = pygame.transform.scale(self.default_sprite, (self.width, self.height))
    
    def setPosition(self, new_position):       
        if new_position[0] - self.width // 2 < 0:
            self.position.x = self.width // 2
        elif new_position[0] + self.width // 2 > Constants.SCREEN_WIDTH:
            self.position.x = Constants.SCREEN_WIDTH - self.width // 2
        else:
            self.position.x = new_position[0]
        
        if new_position[1] - self.height // 2 < 0:
            self.position.y = self.height // 2
        elif new_position[1] + self.height // 2 > Constants.BOTTOM_EDGE_OF_SCRREN_SURFACE:
            self.position.y = Constants.BOTTOM_EDGE_OF_SCRREN_SURFACE - self.height // 2
        else:
            self.position.y = new_position[1]
        
        self._updateBBox()
        self._updateSprite()

    def setSize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        self.center_offset = pygame.math.Vector2(self.width // 2, self.height // 2)
        self._updateBBox()
        self._updateSprite()
    
    def setMovable(self, state: bool):
        self.movable = state

    def getPosition(self):
        return self.position

    def getBoundingBox(self):
        return self.bounding_box

    def getSize(self):
        return (self.width, self.height)
    
    def isMovable(self):
        return self.movable
    
    def draw(self, surface):
        pygame.draw.rect(surface=surface, color=self.color, rect=self.bounding_box)
    
    def drawBBox(self, surface):
        pygame.draw.rect(surface=surface, color=Constants.GREEN, rect=self.bounding_box)

    def drawSprite(self, surface):
        pygame.Surface.blit(surface, self.sprite, self.position)