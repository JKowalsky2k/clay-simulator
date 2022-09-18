import Point
import Constants
import copy
import math

class EndPoint(Point.Point):
    def __init__(self, position, radius, color, trajectory) -> None:
        super().__init__(position, radius, color, trajectory)
        self.relative_position = 0
    
    def setPosition(self, new_position):
        self.position = copy.copy(min(self.trajectory.getTrajectory(), key=lambda point: math.sqrt((point.x-new_position[0])**2+(point.y-new_position[1])**2)))

        self.relative_position = self.position - self.trajectory.getFirstPointPosition()
        self.relative_position.x = abs(self.relative_position.x)
        
        self._updateBBox()
        self._updateSprite()

    def updatePosition(self):
        self.position.x = self.trajectory.getFirstPointPosition().x + self.relative_position.x if True == self.trajectory.getDirection() else self.trajectory.getFirstPointPosition().x - self.relative_position.x
        self.position = copy.copy(min(self.trajectory.getTrajectory(), key=lambda point: abs(point.x-self.position.x)))
        self._updateBBox()
        self._updateSprite()

    def fixPosition(self):
        self.position = copy.copy(min(self.trajectory.getTrajectory(), key=lambda point: math.sqrt((point.x-self.position.x)**2+(point.y-self.position.y)**2)))
