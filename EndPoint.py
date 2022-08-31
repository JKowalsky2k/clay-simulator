import Point
import Constants
import copy

class EndPoint(Point.Point):
    def __init__(self, position, radius, color, trajectory) -> None:
        super().__init__(position, radius, color, trajectory)
        self.relative_position = 0

    def getClosestPoint(self, points, ref_x):
        for point in points:
            if int(point[0]) == ref_x:
                return point[1]
    
    def setPosition(self, new_position):
        if new_position[0] < self.trajectory.getFirstPointPosition().x:
            self.position.x = self.trajectory.getFirstPointPosition().x
        elif new_position[0] > self.trajectory.getLastPointPosition().x:
            self.position.x = self.trajectory.getLastPointPosition().x
        else:
            self.position.x = new_position[0]

        self.position = copy.copy(min(self.trajectory.getTrajectory(), key=lambda point: abs(point.x-self.position.x)))

        self.relative_position = self.position - self.trajectory.getFirstPointPosition() 
        self._updateBBox()

    def updatePosition(self):
        self.position.x = self.trajectory.getFirstPointPosition().x + self.relative_position.x
        self.position = copy.copy(min(self.trajectory.getTrajectory(), key=lambda point: abs(point.x-self.position.x)))
        self._updateBBox()
