import pygame
import pygame_gui
import Trajectory
import BackgroundController

class ControlsController:
    def __init__(self, manager, trajectory, background) -> None:
        self.controls = []
        self.manager = manager
        self.trajectory = trajectory
        self.background = background

    def kill(self):
        for control in self.controls:
            control.kill()
        self.controls = []

    def updateContainer(self):
        pass

    def create(self):
        pass

    def event(self, event):
        pass
