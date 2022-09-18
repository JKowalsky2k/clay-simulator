import Point
import Constants

class StartPoint(Point.Point):
    def __init__(self, position, radius, color, trajectory) -> None:
        super().__init__(position, radius, color, trajectory)
    
    def setPosition(self, new_position):
        if new_position[0] - Constants.CLAY_RADIUS < 0:
            self.position.x = Constants.CLAY_RADIUS
        elif new_position[0] + Constants.CLAY_RADIUS > Constants.SCREEN_WIDTH:
            self.position.x = Constants.SCREEN_WIDTH - Constants.CLAY_RADIUS
        else:
            self.position.x = new_position[0]
        
        if new_position[1] - Constants.CLAY_RADIUS < 0:
            self.position.y = Constants.CLAY_RADIUS
        elif new_position[1] + Constants.CLAY_RADIUS > Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT:
            self.position.y = Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT - Constants.CLAY_RADIUS
        else:
            self.position.y = new_position[1]

        self._updateBBox()
        self._updateSprite()