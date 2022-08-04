import pygame
import Constants
import numpy as np 
import math 
import scipy.constants as const 

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

    # TODO: pomyleć nad refaktorem
    def projectile_motion(self, angle=math.pi/4, v0=40, dt=1e-3, gamm=0, h=100):
        vx0 = math.cos(angle)*v0
        vy0 = math.sin(angle)*v0
        time = np.arange(0, 100, dt)
        x = np.zeros(len(time))
        y = np.zeros(len(time))
        x[0], y[0] = 0, 0
        x[1], y[1] = x[0] + vx0*(2*dt), y[0]+vy0*(2*dt)
        i=1 
        while y[i] >= 0:
            f = 0.5 * gamm * (h - y[i]) * dt
            x[i+1] = ((2*x[i]-x[i-1]) + (f * x[i-1])) / (1 + f)
            y[i+1] = ((2*y[i]-y[i-1]) + (f * y[i-1]) - const.g*(dt**2) ) / (1 + f)
            i += 1
        x = x[0:i+1]
        y = y[0:i+1]
        return [pygame.math.Vector2(point[0], -point[1]) + self.start_clay_position for point in list(zip(x, y))]

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