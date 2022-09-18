import Point
import Constants
import SimulationSettings

class StartPoint(Point.Point):
    def __init__(self, position, radius, color, trajectory) -> None:
        super().__init__(position, radius, color, trajectory)
    
    def setPosition(self, new_position):
        if new_position[0] - SimulationSettings.CLAY_SIZE < 0:
            self.position.x = SimulationSettings.CLAY_SIZE
        elif new_position[0] + SimulationSettings.CLAY_SIZE > Constants.SCREEN_WIDTH:
            self.position.x = Constants.SCREEN_WIDTH - SimulationSettings.CLAY_SIZE
        else:
            self.position.x = new_position[0]
        
        if new_position[1] - SimulationSettings.CLAY_SIZE < 0:
            self.position.y = SimulationSettings.CLAY_SIZE
        elif new_position[1] + SimulationSettings.CLAY_SIZE > Constants.BOTTOM_EDGE_OF_SCRREN_SURFACE:
            self.position.y = Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT - SimulationSettings.CLAY_SIZE
        else:
            self.position.y = new_position[1]

        self._updateBBox()
        self._updateSprite()