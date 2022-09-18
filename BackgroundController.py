import pygame
import glob
import os
import Constants

class BackgorundController:
    def __init__(self, path) -> None:
        default_background = pygame.Surface((2000, 2000))
        default_background.fill(Constants.BLACK)
        self.backgorunds = [default_background]
        try:
            self.backgorunds += [pygame.image.load(path) for path in glob.glob(f'{path}/*')]
        except Exception as error:
            print(f"Loading resources error: {error}")
        self.backgorund_index = 0
        self.current_background = self.backgorunds[self.backgorund_index]

    def getBackgroundIndex(self):
        return self.backgorund_index+1

    def next(self):
        if self.backgorund_index < len(self.backgorunds)-1:
            self.backgorund_index += 1
        else:
            self.backgorund_index = 0
        self.current_background = self.backgorunds[self.backgorund_index]

    def previous(self):
        if self.backgorund_index > 0:
            self.backgorund_index -= 1
        else:
            self.backgorund_index = len(self.backgorunds)-1
        self.current_background = self.backgorunds[self.backgorund_index]
    
    def draw(self, surface):
        surface.blit(pygame.transform.scale(self.current_background, (Constants.SCREEN_WIDTH, Constants.BOTTOM_EDGE_OF_SCRREN_SURFACE)), (0, 0))