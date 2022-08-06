import pygame
import Constants
import numpy as np 
import math 
import scipy.constants as const 

class Trajectory():
    def __init__(self, screen, hud_height) -> None:
        self.screen_surface = screen
        self.start_clay_position = pygame.math.Vector2(Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT/2)
        self.stop_clay_position = pygame.math.Vector2(Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT/2)
        self.apogeum_position = pygame.math.Vector2(Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT/2)
        self.hud_height = hud_height
        self.trajectory = []

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

    def projectile_motion(self, angle=45, v0=40, dt=1e-3, gamm=0, h=100, offset=pygame.math.Vector2(0, 0)):
        vx0 = math.cos(np.deg2rad(angle))*v0
        vy0 = math.sin(np.deg2rad(angle))*v0
        x, y = [0], [0]
        x.append(x[-1] + vx0*(2*dt))
        y.append(y[-1] + vy0*(2*dt))
        while y[-1] >= 0:
            f = 0.5 * gamm * (h - y[-1]) * dt
            next_x = ((2*x[-1]-x[-2]) + (f * x[-2])) / (1 + f)
            next_y = ((2*y[-1]-y[-2]) + (f * y[-2]) - const.g*(dt**2)) / (1 + f)
            x.append(next_x)
            y.append(next_y)
        raw_trajectory = [pygame.math.Vector2(point[0], -point[1]) + offset for point in list(zip(x, y))]
        # cut trajectory while out of screen
        self.trajectory = []
        for point in raw_trajectory:
            if point.x < Constants.SCREEN_WIDTH and point.y > 0 and point.x > 0:
                self.trajectory.append(point)
            else:
                break

    def draw(self, surface, gap):
        for idx in range(self.getNumberOfPoints()):
            if idx % gap == 0:
                pygame.draw.circle(surface=surface, 
                                   color=Constants.WHITE, 
                                   center=self.trajectory[idx], 
                                   radius=1)
    
    def getTrajectory(self):
        return self.trajectory
    
    def getNumberOfPoints(self):
        return len(self.trajectory)