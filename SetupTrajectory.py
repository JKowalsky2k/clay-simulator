import pygame

class Trajectory():
    def __init__(self) -> None:
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500
        self.ORANGE = (255, 165,   0)
        self.RED    = (255,   0,   0)
        self.WHITE  = (255, 255, 255)
        self.BLACK  = (  0,   0,   0) 

        self.ground_line_vertical_position = 0

    def setGroundLine(self, mouse_position):
        if mouse_position[1] < 0:
            self.ground_line_vertical_position = 0
        elif mouse_position[1] > self.SCREEN_HEIGHT:
            self.ground_line_vertical_position = self.SCREEN_HEIGHT
        else:
            self.ground_line_vertical_position = mouse_position[1]

    def drawGroundLine(self, screen):
        print(f"{self.ground_line_vertical_position = }")
        pygame.draw.line(surface=screen,
                         color=self.WHITE,
                         start_pos=pygame.math.Vector2(0, self.ground_line_vertical_position),
                         end_pos=pygame.math.Vector2(self.SCREEN_WIDTH, self.ground_line_vertical_position),
                         width=1)