import Point
import Constants
import copy
import math

class EndPoint(Point.Point):
    def __init__(self, position, radius, color, trajectory) -> None:
        super().__init__(position, radius, color, trajectory)
        self.relative_position = 0
    
    def setPosition(self, new_position):
        # if True == self.trajectory.getDirection():
        #     if new_position[0] < self.trajectory.getFirstPointPosition().x:
        #         self.position.x = self.trajectory.getFirstPointPosition().x
        #     elif new_position[0] > self.trajectory.getLastPointPosition().x:
        #         self.position.x = self.trajectory.getLastPointPosition().x
        #     else:
        #         self.position.x = new_position[0]
        # elif False == self.trajectory.getDirection():
        #     if new_position[0] < self.trajectory.getLastPointPosition().x:
        #         self.position.x = self.trajectory.getLastPointPosition().x
        #     elif new_position[0] > self.trajectory.getFirstPointPosition().x:
        #         self.position.x = self.trajectory.getFirstPointPosition().x
        #     else:
        #         self.position.x = new_position[0]            

        # self.position = copy.copy(min(self.trajectory.getTrajectory(), key=lambda point: abs(point.x-self.position.x)))
        self.position = copy.copy(min(self.trajectory.getTrajectory(), key=lambda point: math.sqrt((point.x-new_position[0])**2+(point.y-new_position[1])**2)))

        self.relative_position = self.position - self.trajectory.getFirstPointPosition() 
        self._updateBBox()

    def updatePosition(self):
        self.position.x = self.trajectory.getFirstPointPosition().x + self.relative_position.x
        self.position = copy.copy(min(self.trajectory.getTrajectory(), key=lambda point: abs(point.x-self.position.x)))
        self._updateBBox()
