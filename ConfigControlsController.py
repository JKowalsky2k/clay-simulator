import pygame
import pygame_gui
import ControlsController
import Constants
import TrajectorySettings

class ConfigGUI(ControlsController.ControlsController):
    def __init__(self, manager, trajectory, background) -> None:
        super().__init__(manager, trajectory, background)

    def updateContainer(self):
        self.container.set_position((0, Constants.SCREEN_HEIGHT-Constants.HUD_HEIGHT))
        container_min_width = self.last_control.get_abs_rect()[0] + self.last_control.get_abs_rect()[2] + Constants.PADDING
        self.container.set_dimensions((container_min_width, Constants.HUD_HEIGHT))
        self.container.set_position(((Constants.SCREEN_WIDTH - container_min_width) // 2, Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT))
    
    def create(self):
        self.container = pygame_gui.core.UIContainer(   relative_rect=pygame.Rect(0, Constants.SCREEN_HEIGHT-Constants.HUD_HEIGHT, Constants.SCREEN_WIDTH, Constants.HUD_HEIGHT),
                                                        container=self.manager.get_root_container(),
                                                        manager=self.manager)
        self.controls.append(self.container)

        # Section HUD Velocity
        self.velocity_name_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(10, 10, 90, 20),
                                                                text='Velocity', 
                                                                manager=self.manager,
                                                                container=self.container)
        self.controls.append(self.velocity_name_label)
        self.velocity_value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 40, 90, 20),
                                                                text=f"{self.trajectory.getVelocity()}", 
                                                                manager=self.manager,
                                                                container=self.container)
        self.controls.append(self.velocity_value_label)
        self.velocity_increase_button = pygame_gui.elements.UIButton(   relative_rect=pygame.Rect(10, 70, 40, 20),
                                                                        text='+', 
                                                                        manager=self.manager,
                                                                        container=self.container)
        self.controls.append(self.velocity_increase_button)
        self.velocity_decrease_button = pygame_gui.elements.UIButton(   relative_rect=pygame.Rect(60, 70, 40, 20),
                                                                        text='-', 
                                                                        manager=self.manager,
                                                                        container=self.container)
        self.controls.append(self.velocity_decrease_button)

        # Section HUD Angle
        self.angle_name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(110, 10, 90, 20),
                                                            text='Angle (\u00B0)', 
                                                            manager=self.manager,
                                                            container=self.container)
        self.controls.append(self.angle_name_label)
        self.angle_value_label = pygame_gui.elements.UILabel(   relative_rect=pygame.Rect(110, 40, 90, 20),
                                                                text=f"{round(self.trajectory.getAngle(), 2)}", 
                                                                manager=self.manager,
                                                                container=self.container)
        self.controls.append(self.angle_value_label)
        self.angle_increase_button = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(110, 70, 40, 20),
                                                                    text='+', 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.angle_increase_button)
        self.angle_decrease_button = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(160, 70, 40, 20),
                                                                    text='-', 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.angle_decrease_button)

        # Section HUD Air Drag
        self.air_drag_name_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(210, 10, 90, 20),
                                                            text='Air Drag', 
                                                            manager=self.manager,
                                                            container=self.container)
        self.controls.append(self.air_drag_name_label)
        self.air_drag_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(210, 40, 90, 50),
                                                            text='Enable', 
                                                            manager=self.manager,
                                                            container=self.container)
        self.air_drag_button.set_text("Disable") if self.trajectory.isDrag() else self.air_drag_button.set_text("Enable")
        self.controls.append(self.air_drag_button)

        # Section Background
        self.background_name_label = pygame_gui.elements.UILabel(   relative_rect=pygame.Rect(310, 10, 90, 20),
                                                                    text='Background', 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.background_name_label)
        self.background_value_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(310, 40, 90, 20),
                                                                    text=f"{self.background.getBackgroundIndex()}", 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.background_value_label)
        self.background_button_previous = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(310, 70, 40, 20),
                                                                        text='<', 
                                                                        manager=self.manager,
                                                                        container=self.container)
        self.controls.append(self.background_button_previous)
        self.background_button_next = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(360, 70, 40, 20),
                                                                    text='>',
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.background_button_next)

        # Section HUD Start
        self.last_control = self.start_button = pygame_gui.elements.UIButton(   relative_rect=pygame.Rect(410, 10, 90, 80),
                                                                                text='Start', 
                                                                                manager=self.manager,
                                                                                container=self.container)
        self.controls.append(self.start_button)

    def event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Velocity
            if event.ui_element == self.velocity_increase_button:
                if self.trajectory.getVelocity() < TrajectorySettings.VELOCITY_MAX:
                    self.trajectory.setVelocity(self.trajectory.getVelocity() + TrajectorySettings.VELOCITY_STEP)
                    self.velocity_value_label.set_text(f"{self.trajectory.getVelocity()}")
            if event.ui_element == self.velocity_decrease_button:
                if self.trajectory.getVelocity() > 0:
                    self.trajectory.setVelocity(self.trajectory.getVelocity() - TrajectorySettings.VELOCITY_STEP)
                    self.velocity_value_label.set_text(f"{self.trajectory.getVelocity()}")
            # Angle
            if event.ui_element == self.angle_increase_button:
                if self.trajectory.getAngle() < TrajectorySettings.ANGLE_MAX:
                    self.trajectory.setAngle(self.trajectory.getAngle() + TrajectorySettings.ANGLE_STEP)
                else:
                    self.trajectory.setAngle(0)
                self.angle_value_label.set_text(f"{round(self.trajectory.getAngle(), 2)}")
            if event.ui_element == self.angle_decrease_button:
                if self.trajectory.getAngle() > 0:
                    self.trajectory.setAngle(self.trajectory.getAngle() - TrajectorySettings.ANGLE_STEP)
                else:
                    self.trajectory.setAngle(TrajectorySettings.ANGLE_MAX)
                self.angle_value_label.set_text(f"{round(self.trajectory.getAngle(), 2)}")
            # Air Drag
            if event.ui_element == self.air_drag_button:
                if self.trajectory.isDrag() == True:
                    self.trajectory.setDrag(False)
                    self.air_drag_button.set_text("Enable")
                else:
                    self.trajectory.setDrag(True)
                    self.air_drag_button.set_text("Disable")
            # Background
            if event.ui_element == self.background_button_next:
                self.background.next()
                self.background_value_label.set_text(f"{self.background.getBackgroundIndex()}")
            if event.ui_element == self.background_button_previous:
                self.background.previous()
                self.background_value_label.set_text(f"{self.background.getBackgroundIndex()}")               
            # Start
            if event.ui_element == self.start_button:
                self.kill()
                return True
            return False
