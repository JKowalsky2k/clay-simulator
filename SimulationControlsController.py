import pygame
import pygame_gui
import ControlsController
import Constants
import SimulationSettings
import json

class SimulationGUI(ControlsController.ControlsController):
    def __init__(self, manager, trajectory, background, clay) -> None:
        super().__init__(manager, trajectory, background)
        self.clay = clay
        with open("settings/settings.json") as settings_file:
            self.settings = json.load(settings_file)
    
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

        # Section HUD Simulation Speed
        self.simulation_speed_name_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(10, 10, 90, 20),
                                                                        text='Speed', 
                                                                        manager=self.manager,
                                                                        container=self.container)
        self.controls.append(self.simulation_speed_name_label)
        self.simulation_speed_value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 40, 90, 20),
                                                                        text=f"{SimulationSettings.SPEED}", 
                                                                        manager=self.manager,
                                                                        container=self.container)
        self.controls.append(self.simulation_speed_value_label)
        self.simulation_speed_increase_button = pygame_gui.elements.UIButton(   relative_rect=pygame.Rect(10, 70, 40, 20),
                                                                                text='+', 
                                                                                manager=self.manager,
                                                                                container=self.container)
        self.controls.append(self.simulation_speed_increase_button)
        self.simulation_speed_decrease_button = pygame_gui.elements.UIButton(   relative_rect=pygame.Rect(60, 70, 40, 20),
                                                                                text='-', 
                                                                                manager=self.manager,
                                                                                container=self.container)
        self.controls.append(self.simulation_speed_decrease_button)  

        # Section HUD Clay size
        self.size_name_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(110, 10, 90, 20),
                                                            text='Size', 
                                                            manager=self.manager,
                                                            container=self.container)
        self.controls.append(self.size_name_label)
        self.size_value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(110, 40, 90, 20),
                                                            text=f"{SimulationSettings.CLAY_SIZE}", 
                                                            manager=self.manager,
                                                            container=self.container)
        self.controls.append(self.size_value_label)
        self.size_increase_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(110, 70, 40, 20),
                                                            text='+', 
                                                            manager=self.manager,
                                                            container=self.container)
        self.controls.append(self.size_increase_button)
        self.size_decrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(160, 70, 40, 20),
                                                            text='-', 
                                                            manager=self.manager,
                                                            container=self.container)
        self.controls.append(self.size_decrease_button)
              
        # Section HUD Visibility
        self.visibility_name_label = pygame_gui.elements.UILabel(   relative_rect=pygame.Rect(210, 10, 90, 20),
                                                                    text='Visibility', 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.visibility_name_label)
        self.visibility_button = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(210, 40, 90, 50),
                                                                text='Disable', 
                                                                manager=self.manager,
                                                                container=self.container)
        self.controls.append(self.visibility_button)

        # Section HUD Pause
        self.pause_name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(310, 10, 90, 20),
                                                            text='Pause', 
                                                            manager=self.manager,
                                                            container=self.container)
        self.controls.append(self.pause_name_label)
        self.pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(310, 40, 90, 50),
                                                         text='Enable', 
                                                         manager=self.manager,
                                                         container=self.container)
        self.controls.append(self.pause_button)

        # Section Background
        self.background_name_label = pygame_gui.elements.UILabel(   relative_rect=pygame.Rect(410, 10, 90, 20),
                                                                    text='Background', 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.background_name_label)
        self.background_value_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(410, 40, 90, 20),
                                                                    text=f"{self.background.getBackgroundIndex()}", 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.background_value_label)
        self.background_button_previous = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(410, 70, 40, 20),
                                                                        text='<', 
                                                                        manager=self.manager,
                                                                        container=self.container)
        self.controls.append(self.background_button_previous)
        self.background_button_next = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(460, 70, 40, 20),
                                                                    text='>',
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.background_button_next)



        # Section HUD Trajectory Selection
        self.trajectory_name_label = pygame_gui.elements.UILabel(   relative_rect=pygame.Rect(510, 10, 90, 20),
                                                                    text='Trajectory', 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.trajectory_name_label)
        self.trajectory_value_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(510, 40, 90, 20),
                                                                    text=f"{0}", 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.trajectory_value_label)
        self.trajectory_button_previous = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(510, 70, 40, 20),
                                                                        text='<', 
                                                                        manager=self.manager,
                                                                        container=self.container)
        self.controls.append(self.trajectory_button_previous)
        self.trajectory_button_next = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(560, 70, 40, 20),
                                                                    text='>', 
                                                                    manager=self.manager,
                                                                    container=self.container)
        self.controls.append(self.trajectory_button_next)
        
        # Section Start Mode
        self.start_mode_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(610, 10, 90, 20),
                                                        text='Start Mode', 
                                                        manager=self.manager,
                                                        container=self.container)
        self.controls.append(self.start_mode_label)
        self.start_mode_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(610, 40, 90, 50),
                                                              text=SimulationSettings.START_MODE, 
                                                              manager=self.manager,
                                                              container=self.container)
        self.controls.append(self.start_mode_button)

        # Section HUD Reset
        self.last_control = self.reset_button = pygame_gui.elements.UIButton(   relative_rect=pygame.Rect(710, 10, 90, 80),
                                                                                text='Reset', 
                                                                                manager=self.manager,
                                                                                container=self.container)
        self.controls.append(self.reset_button)

    def event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Size
            if event.ui_element == self.size_increase_button:
                if SimulationSettings.CLAY_SIZE < self.settings["clay_size"]["max"]:
                    SimulationSettings.CLAY_SIZE += self.settings["clay_size"]["step"]
                    self.size_value_label.set_text(f"{round(SimulationSettings.CLAY_SIZE, 2)}")
                    self.clay.setRadius(SimulationSettings.CLAY_SIZE)
            if event.ui_element == self.size_decrease_button:
                if SimulationSettings.CLAY_SIZE > self.settings["clay_size"]["min"]:
                    SimulationSettings.CLAY_SIZE -= self.settings["clay_size"]["step"]
                    self.size_value_label.set_text(f"{round(SimulationSettings.CLAY_SIZE, 2)}")
                    self.clay.setRadius(SimulationSettings.CLAY_SIZE)
            # Simulation Speed
            if event.ui_element == self.simulation_speed_increase_button:
                if SimulationSettings.SPEED < self.settings["simulation_speed"]["max"]:
                    SimulationSettings.SPEED += self.settings["simulation_speed"]["step"]
                    if SimulationSettings.SPEED > 0:
                        self.pause_button.enable()
                    self.simulation_speed_value_label.set_text(f"{SimulationSettings.SPEED}")
            if event.ui_element == self.simulation_speed_decrease_button:
                if SimulationSettings.SPEED > 0:
                    SimulationSettings.SPEED -= self.settings["simulation_speed"]["step"]
                    if SimulationSettings.SPEED <= 0:
                        SimulationSettings.SPEED = 0
                        self.pause_button.disable()
                    self.simulation_speed_value_label.set_text(f"{SimulationSettings.SPEED}")
            # Visibility
            if event.ui_element == self.visibility_button:
                if SimulationSettings.VISIBILITY == True:
                    SimulationSettings.VISIBILITY = False
                    self.visibility_button.set_text("Enable")
                else:
                    SimulationSettings.VISIBILITY = True
                    self.visibility_button.set_text("Disable")
            # Pause
            if event.ui_element == self.pause_button:
                if SimulationSettings.PAUSE == True:
                    SimulationSettings.PAUSE = False
                    self.pause_button.set_text("Enable")
                    self.simulation_speed_increase_button.enable()
                    self.simulation_speed_decrease_button.enable()
                    SimulationSettings.SPEED = SimulationSettings.PREVIOUS_SPEED
                else:
                    SimulationSettings.PAUSE = True
                    SimulationSettings.PREVIOUS_SPEED = SimulationSettings.SPEED
                    SimulationSettings.SPEED = 0
                    self.pause_button.set_text("Disable")
                    self.simulation_speed_increase_button.disable()
                    self.simulation_speed_decrease_button.disable()
                self.simulation_speed_value_label.set_text(f"{SimulationSettings.SPEED}")
            # Background
            if event.ui_element == self.background_button_next:
                self.background.next()
                self.background_value_label.set_text(f"{self.background.getBackgroundIndex()}")
            if event.ui_element == self.background_button_previous:
                self.background.previous()
                self.background_value_label.set_text(f"{self.background.getBackgroundIndex()}")
            # Start Mode
            if event.ui_element == self.start_mode_button:
                if SimulationSettings.START_MODE == "Auto":
                    self.start_mode_button.set_text("Manual")
                    SimulationSettings.START_MODE = "Manual"
                else:
                    self.start_mode_button.set_text("Auto")
                    SimulationSettings.START_MODE = "Auto"

            # Reset
            if event.ui_element == self.reset_button:
                self.kill()
                return True
            return False