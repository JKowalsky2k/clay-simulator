import pygame
import Constants

class Trajectory():
    def __init__(self, screen, hud_height) -> None:
        self.screen = screen
        self.start_clay_position = pygame.math.Vector2(Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT/2)
        self.stop_clay_position = pygame.math.Vector2(Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT/2)
        self.apogeum_position = pygame.math.Vector2(Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT/2)
        self.hud_height = hud_height

    def setStartClayPosition(self, mouse_position):
        if mouse_position[0] - Constants.CLAY_RADIUS < 0:
            self.start_clay_position.x = Constants.CLAY_RADIUS
        elif mouse_position[0] + Constants.CLAY_RADIUS > Constants.SCREEN_WIDTH:
            self.start_clay_position.x = Constants.SCREEN_WIDTH - Constants.CLAY_RADIUS
        else:
            self.start_clay_position.x = mouse_position[0]
        
        if mouse_position[1] - Constants.CLAY_RADIUS < 0:
            self.start_clay_position.y = Constants.CLAY_RADIUS
        elif mouse_position[1] + Constants.CLAY_RADIUS > Constants.SCREEN_HEIGHT - self.hud_height:
            self.start_clay_position.y = Constants.SCREEN_HEIGHT - self.hud_height - Constants.CLAY_RADIUS
        else:
            self.start_clay_position.y = mouse_position[1]

    def setStopClayPosition(self, mouse_position):
        if mouse_position[0] - Constants.CLAY_RADIUS < self.start_clay_position.x:
            self.stop_clay_position.x = self.start_clay_position.x
        elif mouse_position[0] + Constants.CLAY_RADIUS > Constants.SCREEN_WIDTH:
            self.stop_clay_position.x = Constants.SCREEN_WIDTH - Constants.CLAY_RADIUS
        else:
            self.stop_clay_position.x = mouse_position[0]
        
        if mouse_position[1] - Constants.CLAY_RADIUS < 0:
            self.stop_clay_position.y = Constants.CLAY_RADIUS
        elif mouse_position[1] + Constants.CLAY_RADIUS > Constants.SCREEN_HEIGHT - self.hud_height:
            self.stop_clay_position.y = Constants.SCREEN_HEIGHT - self.hud_height - Constants.CLAY_RADIUS
        else:
            self.stop_clay_position.y = mouse_position[1]

    def setApogeum(self, mouse_position):
        if mouse_position[0] - Constants.CLAY_RADIUS < self.start_clay_position.x:
            self.apogeum_position.x = self.start_clay_position.x
        elif mouse_position[0] + Constants.CLAY_RADIUS > self.stop_clay_position.x:
            self.apogeum_position.x = self.stop_clay_position.x
        else:
            self.apogeum_position.x = mouse_position[0]
        
        if mouse_position[1] - Constants.CLAY_RADIUS < 0:
            self.apogeum_position.y = Constants.CLAY_RADIUS 
        elif mouse_position[1] + Constants.CLAY_RADIUS > Constants.SCREEN_HEIGHT - self.hud_height:
            self.apogeum_position.y = Constants.SCREEN_HEIGHT - self.hud_height - Constants.CLAY_RADIUS
        else:
            self.apogeum_position.y = mouse_position[1]

    def drawStartClayPosition(self):
        pygame.draw.circle(surface=self.screen,
                           color=Constants.RED, 
                           center=pygame.math.Vector2(self.start_clay_position),
                           radius=Constants.CLAY_RADIUS)

    def drawStopClayPosition(self):
        pygame.draw.circle(surface=self.screen,
                           color=Constants.BLUE, 
                           center=pygame.math.Vector2(self.stop_clay_position),
                           radius=Constants.CLAY_RADIUS)
    
    def drawApogeum(self):
        pygame.draw.circle(surface=self.screen,
                           color=Constants.GREEN, 
                           center=self.apogeum_position,
                           radius=Constants.CLAY_RADIUS)
    
    def getGroundLineVerticalPosition(self):
        return self.ground_line_vertical_position
 
    def getStartClayPosition(self):
        return self.start_clay_position

    def getStopClayPosition(self):
        return self.stop_clay_position
    
    def getApogeum(self):
        return self.apogeum_position