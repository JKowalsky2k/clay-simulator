import enum
from sys import float_repr_style
import pygame
import pygame_gui
import SetupTrajectory
import Constants
import Point

class States(enum.Enum):
    CONFIG = 0
    SIMULATION = 1
    RESET = 2
    EXIT = 3

class ConfigStates(enum.Enum):
    START = 0
    STOP = 1
    APOGEUM = 2
    END = 3

class SimulationController:
    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()
        self.FPS = 120

        self.screen = pygame.display.set_mode(size=(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), 
                                              flags=pygame.RESIZABLE)
        self.screen_surface = pygame.display.get_surface()
        Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()

        self.manager = pygame_gui.UIManager(window_resolution=(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), 
                                            theme_path="themes/theme.json")
    
        pygame.display.set_caption('Clay simulator (ver. 6.08.2022)')

        self.update_clay = pygame.USEREVENT
        pygame.time.set_timer(self.update_clay, 1)
       
        self.font = pygame.font.Font("fonts/basic.ttf", 16)
        self.trajectory = SetupTrajectory.Trajectory(self.screen, Constants.HUD_HEIGHT)
        self.state = States.CONFIG

        self.velocity = 40
        self.angle = 45
        self.gamma = 0
        self.size = Constants.CLAY_RADIUS

        self.start_point = Point.Point(position=(Constants.SCREEN_WIDTH//2, Constants.SCREEN_WIDTH//2), 
                                          radius=Constants.CLAY_RADIUS,
                                          color=Constants.RED)
        self.end_point = Point.Point(position=(0, 0), 
                                         radius=Constants.CLAY_RADIUS,
                                         color=Constants.BLUE)
        self.clay = Point.Point(position=(0, 0), 
                                radius=Constants.CLAY_RADIUS,
                                color=Constants.ORANGE)

    def updateResolution(self):
        Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()

    def isResolutionChanged(self):
        if self.screen.get_size() != (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT):
            return True
        return False

    def stateMachine(self) -> None:
        while self.state != States.EXIT:
            if self.state == States.CONFIG:
                self.stateCONFIG()
            elif self.state == States.SIMULATION:
                self.stateSIMULATION()
            elif self.state == States.RESET:
                self.stateRESET()
        print("Bye!")
        pygame.quit()

    def stateCONFIG(self) -> None:
        print(f"{self.state.name = }")
        
        controls = []
        drag = False
        trajectory_elements = [{"object": self.start_point, "drag": False}]

        self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        config_hud_container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect(0, Constants.SCREEN_HEIGHT-Constants.HUD_HEIGHT, Constants.SCREEN_WIDTH, Constants.HUD_HEIGHT),
                                                    container=self.manager.get_root_container(),
                                                    manager=self.manager)
        controls.append(config_hud_container)

        # Section HUD Velocity

        velocity_name_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(10, 10, 90, 20),
                                                            text='Velocity', 
                                                            manager=self.manager,
                                                            container=config_hud_container)
        controls.append(velocity_name_label)

        velocity_value_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(10, 40, 90, 20),
                                                            text=f"{self.velocity}", 
                                                            manager=self.manager,
                                                            container=config_hud_container)
        controls.append(velocity_value_label)
        
        velocity_increase_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(10, 70, 40, 20),
                                                                text='+', 
                                                                manager=self.manager,
                                                                container=config_hud_container)
        controls.append(velocity_increase_button)
        
        velocity_decrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(60, 70, 40, 20),
                                                                text='-', 
                                                                manager=self.manager,
                                                                container=config_hud_container)
        controls.append(velocity_decrease_button)

        # Section HUD Angle

        angle_name_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(110, 10, 90, 20),
                                                        text='Angle (\u00B0)', 
                                                        manager=self.manager,
                                                        container=config_hud_container)
        controls.append(angle_name_label)

        angle_value_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(110, 40, 90, 20),
                                                        text=f"{round(self.angle, 2)}", 
                                                        manager=self.manager,
                                                        container=config_hud_container)
        controls.append(angle_value_label)
        
        angle_increase_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(110, 70, 40, 20),
                                                            text='+', 
                                                            manager=self.manager,
                                                            container=config_hud_container)
        controls.append(angle_increase_button)
        
        angle_decrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(160, 70, 40, 20),
                                                            text='-', 
                                                            manager=self.manager,
                                                            container=config_hud_container)
        controls.append(angle_decrease_button)

        # Section HUD Gamma

        gamma_name_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(210, 10, 90, 20),
                                                        text='Gamma', 
                                                        manager=self.manager,
                                                        container=config_hud_container)
        controls.append(gamma_name_label)

        gamma_value_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(210, 40, 90, 20),
                                                        text=f"{self.gamma}", 
                                                        manager=self.manager,
                                                        container=config_hud_container)
        controls.append(gamma_value_label)
        
        gamma_increase_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(210, 70, 40, 20),
                                                            text='+', 
                                                            manager=self.manager,
                                                            container=config_hud_container)
        controls.append(gamma_increase_button)
        
        gamma_decrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(260, 70, 40, 20),
                                                             text='-', 
                                                             manager=self.manager,
                                                             container=config_hud_container)
        controls.append(gamma_decrease_button)

        last_control = start_button = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(310, 10, 90, 80),
                                                                    text='Start', 
                                                                    manager=self.manager,
                                                                    container=config_hud_container)
        controls.append(start_button)

        right_padding = 10
        config_hud_container_min_width = last_control.get_abs_rect()[0] + last_control.get_abs_rect()[2] + right_padding
        config_hud_container.set_dimensions((config_hud_container_min_width, Constants.HUD_HEIGHT))
        config_hud_container.set_position(((Constants.SCREEN_WIDTH - config_hud_container_min_width) // 2, Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT))

        self.trajectory.projectile_motion(angle=self.angle, 
                                          v0=self.velocity, 
                                          gamm=self.gamma,
                                          dt=1e-2, 
                                          offset=self.start_point.getPosition())
        self.end_point.setPosition(self.trajectory.getLastPointPosition())

        while self.state == States.CONFIG:
            dt = self.clock.tick(self.FPS)
            if self.isResolutionChanged():
                self.updateResolution()
                self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
                self.screen_surface = pygame.display.get_surface()
                config_hud_container.set_position((0, Constants.SCREEN_HEIGHT-Constants.HUD_HEIGHT))
                
                right_padding = 10
                config_hud_container_min_width = last_control.get_abs_rect()[0] + last_control.get_abs_rect()[2] + right_padding
                config_hud_container.set_dimensions((config_hud_container_min_width, Constants.HUD_HEIGHT))
                config_hud_container.set_position(((Constants.SCREEN_WIDTH - config_hud_container_min_width) // 2, Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
                # Event resposible for protects minimum window size
                elif event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.size
                    if screen_width < Constants.MIN_SCREEN_WIDTH:
                        screen_width = Constants.MIN_SCREEN_WIDTH
                    if screen_height < Constants.MIN_SCREEN_HEIGHT:
                        screen_height = Constants.MIN_SCREEN_HEIGHT
                    self.screen = pygame.display.set_mode(  size=(screen_width, screen_height), 
                                                            flags=pygame.RESIZABLE)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for element in trajectory_elements:
                            if element["object"].getBoundingBox().collidepoint(pygame.mouse.get_pos()):
                                element["drag"] = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for element in trajectory_elements:
                            element["drag"] = False
                elif event.type == pygame.MOUSEMOTION:
                    for element in trajectory_elements:
                        if True == element["drag"]:
                            element["object"].setPosition(pygame.mouse.get_pos())
                            self.trajectory.projectile_motion(angle=self.angle, 
                                                              v0=self.velocity, 
                                                              gamm=self.gamma,
                                                              dt=1e-2,
                                                              offset=self.start_point.getPosition())
                            self.end_point.setPosition(self.trajectory.getLastPointPosition())

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # Velocity
                    if event.ui_element == velocity_increase_button:
                        if self.velocity < 80:
                            self.velocity += 1
                            velocity_value_label.set_text(f"{self.velocity}")
                    if event.ui_element == velocity_decrease_button:
                        if self.velocity > 0:
                            self.velocity -= 1
                            velocity_value_label.set_text(f"{self.velocity}")
                    # Angle
                    if event.ui_element == angle_increase_button:
                        if self.angle < 180:
                            self.angle += 7.5
                        else:
                            self.angle = 0
                        angle_value_label.set_text(f"{round(self.angle, 2)}")
                    if event.ui_element == angle_decrease_button:
                        if self.angle > 0:
                            self.angle -= 7.5
                        else:
                            self.angle = 180
                        angle_value_label.set_text(f"{round(self.angle, 2)}")
                    # Gamma
                    if event.ui_element == gamma_increase_button:
                        if self.gamma < 0.01:
                            self.gamma += 0.001
                            gamma_value_label.set_text(f"{self.gamma}")
                    if event.ui_element == gamma_decrease_button:
                        if self.gamma > 0:
                            self.gamma -= 0.001
                            gamma_value_label.set_text(f"{self.gamma}")
                    # Start
                    if event.ui_element == start_button:
                        for control in controls:
                            control.kill()
                        self.state = States.SIMULATION
                    
                    self.trajectory.projectile_motion(angle=self.angle, 
                                                      v0=self.velocity, 
                                                      gamm=self.gamma,
                                                      dt=1e-2,
                                                      offset=self.start_point.getPosition())
                    self.end_point.setPosition(self.trajectory.getLastPointPosition())
                
                self.manager.process_events(event)

            self.manager.update(dt)

            self.screen.fill(Constants.BLACK)

            self.trajectory.draw(self.screen_surface, gap=Constants.CONFIG_TRAJECTORY_GAP)
            # self.start_point.drawBBox(surface=self.screen_surface)
            self.start_point.draw(surface=self.screen_surface)
            self.end_point.draw(surface=self.screen_surface)

            self.manager.draw_ui(self.screen_surface)
     
            pygame.display.flip()

    def stateSIMULATION(self) -> None:
        print(f"{self.state.name = }")

        # size = Constants.CLAY_RADIUS
        visbility_of_characteristic_points = True
        is_pause = False
        store_delta_x = 0
        simulation_speed_step = 1
        idx = 0

        self.trajectory.projectile_motion(angle=self.angle, 
                                    v0=self.velocity, 
                                    gamm=self.gamma,
                                    dt=1e-3,
                                    offset=self.start_point.getPosition())
        self.end_point.setPosition(self.trajectory.getLastPointPosition())

        controls = []

        self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        hud_container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect(0, Constants.SCREEN_HEIGHT-Constants.HUD_HEIGHT, Constants.SCREEN_WIDTH, Constants.HUD_HEIGHT),
                                                    container=self.manager.get_root_container(),
                                                    manager=self.manager)
        controls.append(hud_container)

        # Section HUD Simulation Speed

        simulation_speed_name_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(10, 10, 90, 20),
                                                                    text='Speed', 
                                                                    manager=self.manager,
                                                                    container=hud_container)
        controls.append(simulation_speed_name_label)

        simulation_speed_value_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(10, 40, 90, 20),
                                                                    text=f"{simulation_speed_step}", 
                                                                    manager=self.manager,
                                                                    container=hud_container)
        controls.append(simulation_speed_value_label)
        
        simulation_speed_increase_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(10, 70, 40, 20),
                                                                        text='+', 
                                                                        manager=self.manager,
                                                                        container=hud_container)
        controls.append(simulation_speed_increase_button)
        
        simulation_speed_decrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(60, 70, 40, 20),
                                                                        text='-', 
                                                                        manager=self.manager,
                                                                        container=hud_container)
        controls.append(simulation_speed_decrease_button)  

        # Section HUD Clay size

        size_name_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(110, 10, 90, 20),
                                                        text='Size', 
                                                        manager=self.manager,
                                                        container=hud_container)
        controls.append(size_name_label)

        size_value_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(110, 40, 90, 20),
                                                        text=f"{self.size}", 
                                                        manager=self.manager,
                                                        container=hud_container)
        controls.append(size_value_label)
        
        size_increase_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(110, 70, 40, 20),
                                                            text='+', 
                                                            manager=self.manager,
                                                            container=hud_container)
        controls.append(size_increase_button)
        
        size_decrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(160, 70, 40, 20),
                                                            text='-', 
                                                            manager=self.manager,
                                                            container=hud_container)
        controls.append(size_decrease_button)
              
        # Section HUD Visibility

        visibility_name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(210, 10, 90, 20),
                                                            text='Visibility', 
                                                            manager=self.manager,
                                                            container=hud_container)
        controls.append(visibility_name_label)

        visibility_button = pygame_gui.elements.UIButton(   relative_rect=pygame.Rect(210, 40, 90, 50),
                                                            text='Disable', 
                                                            manager=self.manager,
                                                            container=hud_container)
        controls.append(visibility_button)

        # Section HUD Pause

        pause_name_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(310, 10, 90, 20),
                                                        text='Pause', 
                                                        manager=self.manager,
                                                        container=hud_container)
        controls.append(pause_name_label)

        pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(310, 40, 90, 50),
                                                    text='Enable', 
                                                    manager=self.manager,
                                                    container=hud_container)
        controls.append(pause_button)

        # Section HUD Trajectory Selection

        trajectory_selection_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(410, 10, 260, 20),
                                                                  text='Trajectory', 
                                                                  manager=self.manager,
                                                                  container=hud_container)
        controls.append(trajectory_selection_label)                                                                    

        trajectory_1_selection = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(410, 40, 50, 50),
                                                                text='1', 
                                                                manager=self.manager,
                                                                container=hud_container,
                                                                object_id=pygame_gui.core.ObjectID(object_id="#trajectory_button"))
        controls.append(trajectory_1_selection)

        trajectory_2_selection = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(480, 40, 50, 50),
                                                                text='2', 
                                                                manager=self.manager,
                                                                container=hud_container,
                                                                object_id=pygame_gui.core.ObjectID(object_id="#trajectory_button"))
        controls.append(trajectory_2_selection)

        trajectory_3_selection = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(550, 40, 50, 50),
                                                                text='3', 
                                                                manager=self.manager,
                                                                container=hud_container,
                                                                object_id=pygame_gui.core.ObjectID(object_id="#trajectory_button"))
        controls.append(trajectory_3_selection)
        
        trajectory_4_selection = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(620, 40, 50, 50),
                                                                text='4', 
                                                                manager=self.manager,
                                                                container=hud_container,
                                                                object_id=pygame_gui.core.ObjectID(object_id="#trajectory_button"))
        controls.append(trajectory_4_selection)

        # Section HUD Reset

        last_control = reset_button = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(680, 10, 90, 80),
                                                                    text='Reset', 
                                                                    manager=self.manager,
                                                                    container=hud_container)
        controls.append(reset_button)

        right_padding = 10
        hud_container_min_width = last_control.get_abs_rect()[0] + last_control.get_abs_rect()[2] + right_padding
        hud_container.set_dimensions((hud_container_min_width, Constants.HUD_HEIGHT))
        hud_container.set_position(((Constants.SCREEN_WIDTH - hud_container_min_width) // 2, Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT))
        
        while self.state == States.SIMULATION:
            dt = self.clock.tick(self.FPS)
            if self.isResolutionChanged():
                self.updateResolution()
                self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
                self.screen_surface = pygame.display.get_surface()
                hud_container.set_position((0, Constants.SCREEN_HEIGHT-Constants.HUD_HEIGHT))
                
                right_padding = 10
                hud_container_min_width = last_control.get_abs_rect()[0] + last_control.get_abs_rect()[2] + right_padding
                hud_container.set_dimensions((hud_container_min_width, Constants.HUD_HEIGHT))
                hud_container.set_position(((Constants.SCREEN_WIDTH - hud_container_min_width) // 2, Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
                # Event resposible for protects minimum window size
                elif event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.size
                    if screen_width < Constants.MIN_SCREEN_WIDTH:
                        screen_width = Constants.MIN_SCREEN_WIDTH
                    if screen_height < Constants.MIN_SCREEN_HEIGHT:
                        screen_height = Constants.MIN_SCREEN_HEIGHT
                    self.screen = pygame.display.set_mode(  size=(screen_width, screen_height), 
                                                            flags=pygame.RESIZABLE)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = States.EXIT

                if event.type == self.update_clay:
                    if idx + simulation_speed_step < self.trajectory.getNumberOfPoints():
                        idx += simulation_speed_step
                    else:
                        idx = 0
                    self.clay.setPosition(self.trajectory.getTrajectory()[idx])

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # Size
                    if event.ui_element == size_increase_button:
                        if self.size < 40:
                            self.size += 1
                            size_value_label.set_text(f"{round(self.size, 2)}")
                            self.clay.setRadius(self.size)
                    if event.ui_element == size_decrease_button:
                        if self.size > 2:
                            self.size -= 1
                            size_value_label.set_text(f"{round(self.size, 2)}")
                            self.clay.setRadius(self.size)
                    # Simulation Speed
                    if event.ui_element == simulation_speed_increase_button:
                        if simulation_speed_step < 20:
                            simulation_speed_step += 1
                            if simulation_speed_step > 0:
                                pause_button.enable()
                            simulation_speed_value_label.set_text(f"{simulation_speed_step}")
                    if event.ui_element == simulation_speed_decrease_button:
                        if simulation_speed_step > 0:
                            simulation_speed_step -= 1
                            if simulation_speed_step == 0:
                                pause_button.disable()
                            simulation_speed_value_label.set_text(f"{simulation_speed_step}")
                    # Visibility
                    if event.ui_element == visibility_button:
                        if visbility_of_characteristic_points == True:
                            visbility_of_characteristic_points = False
                            visibility_button.set_text("Enable")
                        else:
                            visbility_of_characteristic_points = True
                            visibility_button.set_text("Disable")
                    # Pause
                    if event.ui_element == pause_button:
                        if is_pause == True:
                            is_pause = False
                            pause_button.set_text("Enable")
                            simulation_speed_increase_button.enable()
                            simulation_speed_decrease_button.enable()
                            simulation_speed_step = store_delta_x
                        else:
                            is_pause = True
                            store_delta_x = simulation_speed_step
                            simulation_speed_step = 0
                            pause_button.set_text("Disable")
                            simulation_speed_increase_button.disable()
                            simulation_speed_decrease_button.disable()
                        simulation_speed_value_label.set_text(f"{simulation_speed_step}")
                    # Reset
                    if event.ui_element == reset_button:
                        self.state = States.CONFIG
                        for control in controls:
                            control.kill()
                        print(f"Killed all controls: {len(controls)}")                            

                self.manager.process_events(event)

            self.manager.update(dt)

            self.screen_surface.fill(Constants.BLACK)
            
            if visbility_of_characteristic_points == True:
                self.trajectory.draw(self.screen_surface, gap=Constants.SIMULATION_TRAJECTORY_GAP)
            self.start_point.draw(self.screen_surface)
            self.end_point.draw(surface=self.screen_surface)
            self.clay.draw(surface=self.screen_surface)

            self.manager.draw_ui(self.screen_surface)

            pygame.display.flip()

    def stateRESET(self) -> None:
        print(f"{self.state.name = }")
        while self.state == States.RESET:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

    def translate(self, vector) -> pygame.math.Vector2:
        return pygame.math.Vector2(vector.x, Constants.SCREEN_HEIGHT - vector.y)

    def translate_tuple(self, vector) -> tuple:
        return (vector[0], Constants.SCREEN_WIDTH - vector[1])
    
    def translateToPixel(self, vector) -> tuple:
        v = pygame.math.Vector2(vector.x, Constants.SCREEN_HEIGHT - vector.y)
        return (int(v.x), int(v.y))

    def run(self) -> None:
        self.stateMachine()