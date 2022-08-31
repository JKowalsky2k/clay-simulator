import pygame
import Constants
import numpy as np 
import math 
import scipy.constants
import copy

class Trajectory():
    def __init__(self) -> None:
        self.trajectory = []
        self.angle = 45
        self.velocity = 40
        self.offset = pygame.math.Vector2(0, 0)
        self.drag = False
        self.dt = 1e-3

    def setAngle(self, new_angle):
        self.angle = new_angle
    
    def getAngle(self):
        return self.angle

    def setVelocity(self, new_velocity):
        
        self.velocity = new_velocity
    
    def getVelocity(self):
        return self.velocity

    def setOffset(self, new_offset):
        self.offset = new_offset

    def getOffset(self):
        return self.offset

    def setDrag(self, is_drag):
        self.drag = is_drag
    
    def isDrag(self):
        return self.drag

    def setDt(self, new_dt):
        self.dt = new_dt

    def getDt(self):
        return self.dt
    
    def _checkWhenOutOfScreen(self, point):
        point = pygame.math.Vector2(point[0], -point[1]) + self.offset
        if point.x < Constants.SCREEN_WIDTH and \
            point.x > 0 and \
            point.y > 0 and \
            point.y < Constants.SCREEN_HEIGHT-Constants.HUD_HEIGHT:
            return False
        return True


    def calculate(self):
        velocity = copy.copy(self.velocity)
        velocity_x = np.cos(np.deg2rad(self.angle))*velocity
        velocity_y = np.sin(np.deg2rad(self.angle))*velocity

        idx = 0
        pos = np.zeros(shape=(1_000_000, 2))

        while pos[idx, 1] >= -Constants.BOTTOM_EDGE_OF_SCRREN_SURFACE:
            if self.drag:
                ax = -(Constants.D/Constants.MASS)*velocity*velocity_x
                ay = -scipy.constants.g-(Constants.D/Constants.MASS)*velocity*velocity_y
            else:
                ax = 0
                ay = -scipy.constants.g
            velocity_x += ax * self.dt
            velocity_y += ay * self.dt
            velocity = np.sqrt(velocity_x**2 + velocity_y**2)

            pos[idx+1, 0] = pos[idx, 0] + velocity_x*self.dt + 0.5*ax*self.dt**2
            pos[idx+1, 1] = pos[idx, 1] + velocity_y*self.dt + 0.5*ay*self.dt**2
            
            # optymalization
            if True == self._checkWhenOutOfScreen(pos[idx+1, :]):
                break

            idx += 1

        pos = pos[:idx]

        self.trajectory = [pygame.math.Vector2(point[0], -point[1]) + self.offset for point in pos]

    def draw(self, surface, gap):
        for idx in range(self.getNumberOfPoints()):
            if idx % gap == 0:
                pygame.draw.circle(surface=surface, 
                                   color=Constants.WHITE, 
                                   center=self.trajectory[idx], 
                                   radius=1)
    
    def getTrajectory(self):
        return self.trajectory
    
    def getFirstPointPosition(self):
        return self.trajectory[0]

    def getLastPointPosition(self):
        return self.trajectory[-1]
    
    def getNumberOfPoints(self):
        return len(self.trajectory)