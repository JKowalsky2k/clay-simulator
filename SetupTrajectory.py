import pygame
import Constants

class Trajectory():
    def __init__(self) -> None:
        self.ground_line_vertical_position = 0
        self.start_clay_position = pygame.math.Vector2(Constants.SCREEN_WIDTH/2, self.ground_line_vertical_position)
        self.stop_clay_position = pygame.math.Vector2(Constants.SCREEN_WIDTH/2, self.ground_line_vertical_position)
        self.apogeum_position = pygame.math.Vector2(Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT/2)

    def setGroundLine(self, mouse_position):
        if mouse_position[1] < 0:
            self.ground_line_vertical_position = 0
        elif mouse_position[1] > Constants.SCREEN_HEIGHT:
            self.ground_line_vertical_position = Constants.SCREEN_HEIGHT
        else:
            self.ground_line_vertical_position = mouse_position[1]

    def setStartClayPosition(self, mouse_position):
        self.start_clay_position.y = self.ground_line_vertical_position
        if mouse_position[0] - Constants.CLAY_RADIUS < 0:
            self.start_clay_position.x = Constants.CLAY_RADIUS
        elif mouse_position[0] + Constants.CLAY_RADIUS > Constants.SCREEN_WIDTH:
            self.start_clay_position.x = Constants.SCREEN_WIDTH - Constants.CLAY_RADIUS
        else:
            self.start_clay_position.x = mouse_position[0]

    def setStopClayPosition(self, mouse_position):
        self.stop_clay_position.y = self.ground_line_vertical_position
        if mouse_position[0] - Constants.CLAY_RADIUS < self.start_clay_position.x:
            self.stop_clay_position.x = self.start_clay_position.x
        elif mouse_position[0] + Constants.CLAY_RADIUS > Constants.SCREEN_WIDTH:
            self.stop_clay_position.x = Constants.SCREEN_WIDTH - Constants.CLAY_RADIUS
        else:
            self.stop_clay_position.x = mouse_position[0]

    def setApogeum(self, mouse_position):
        if mouse_position[0] - Constants.CLAY_RADIUS < 0:
            self.apogeum_position.x = Constants.CLAY_RADIUS
        elif mouse_position[0] + Constants.CLAY_RADIUS > Constants.SCREEN_WIDTH:
            self.apogeum_position.x = Constants.SCREEN_WIDTH - Constants.CLAY_RADIUS
        elif mouse_position[1] + Constants.CLAY_RADIUS/2 > self.ground_line_vertical_position:
            self.apogeum_position.y = self.ground_line_vertical_position
        elif mouse_position[1] - Constants.CLAY_RADIUS < 0:
            self.apogeum_position.y = Constants.CLAY_RADIUS
        else:
            self.apogeum_position = pygame.math.Vector2(mouse_position[0], mouse_position[1])


    def drawGroundLine(self, screen):
        pygame.draw.line(surface=screen,
                         color=Constants.WHITE,
                         start_pos=pygame.math.Vector2(0, self.ground_line_vertical_position),
                         end_pos=pygame.math.Vector2(Constants.SCREEN_WIDTH, self.ground_line_vertical_position),
                         width=1)

    def drawStartClayPosition(self, screen):
        pygame.draw.circle(surface=screen,
                           color=Constants.RED, 
                           center=pygame.math.Vector2(self.start_clay_position.x, self.ground_line_vertical_position),
                           radius=Constants.CLAY_RADIUS)

    def drawStopClayPosition(self, screen):
        pygame.draw.circle(surface=screen,
                           color=Constants.BLUE, 
                           center=pygame.math.Vector2(self.stop_clay_position.x, self.ground_line_vertical_position),
                           radius=Constants.CLAY_RADIUS)
    
    def drawApogeum(self, screen):
        pygame.draw.circle(surface=screen,
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