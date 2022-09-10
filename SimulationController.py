from time import time
import pygame
import pygame_gui
import enum
import Trajectory
import Constants
import Point
import StartPoint
import EndPoint

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
        self.FPS = 60

        self.screen = pygame.display.set_mode(size=(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), 
                                              flags=pygame.RESIZABLE)
        self.screen_surface = pygame.display.get_surface()
        Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()

        self.manager = pygame_gui.UIManager(window_resolution=(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), 
                                            theme_path="themes/theme.json")
    
        pygame.display.set_caption('Clay simulator (ver. 31.08.2022)')

        self.update_clay = pygame.USEREVENT + 0
       
        self.trajectory = Trajectory.Trajectory()
        self.state = States.CONFIG

        self.size = Constants.CLAY_RADIUS

        self.start_point = StartPoint.StartPoint( position=(Constants.SCREEN_WIDTH//3, Constants.SCREEN_HEIGHT/2), 
                                                  radius=Constants.CLAY_RADIUS,
                                                  color=Constants.RED,
                                                  trajectory=self.trajectory)
        self.end_point = EndPoint.EndPoint( position=(0, 0), 
                                            radius=Constants.CLAY_RADIUS,
                                            color=Constants.BLUE,
                                            trajectory=self.trajectory)
        self.clay = Point.Point(position=(0, 0), 
                                radius=Constants.CLAY_RADIUS,
                                color=Constants.ORANGE,
                                trajectory=self.trajectory)

    def updateResolution(self):
        Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()

    def isResolutionChanged(self):
        return True if self.screen.get_size() != (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT) else False

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

        self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        config_hud_container = pygame_gui.core.UIContainer( relative_rect=pygame.Rect(0, Constants.SCREEN_HEIGHT-Constants.HUD_HEIGHT, Constants.SCREEN_WIDTH, Constants.HUD_HEIGHT),
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
                                                            text=f"{self.trajectory.getVelocity()}", 
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
                                                        text=f"{round(self.trajectory.getAngle(), 2)}", 
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

        # Section HUD Air Drag

        air_drag_name_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(210, 10, 90, 20),
                                                            text='Air Drag', 
                                                            manager=self.manager,
                                                            container=config_hud_container)
        controls.append(air_drag_name_label)

        air_drag_button = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(210, 40, 90, 50),
                                                        text='Enable', 
                                                        manager=self.manager,
                                                        container=config_hud_container)
        air_drag_button.set_text("Disable") if self.trajectory.isDrag() else air_drag_button.set_text("Enable")
        controls.append(air_drag_button)

        # Section HUD Start

        last_control = start_button = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(310, 10, 90, 80),
                                                                    text='Start', 
                                                                    manager=self.manager,
                                                                    container=config_hud_container)
        controls.append(start_button)

        right_padding = 10
        config_hud_container_min_width = last_control.get_abs_rect()[0] + last_control.get_abs_rect()[2] + right_padding
        config_hud_container.set_dimensions((config_hud_container_min_width, Constants.HUD_HEIGHT))
        config_hud_container.set_position(((Constants.SCREEN_WIDTH - config_hud_container_min_width) // 2, Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT))

        self.trajectory.setDt(1e-2)
        self.trajectory.setOffset(self.start_point.getPosition())
        self.trajectory.calculate()
        self.end_point.setPosition(self.trajectory.getLastPointPosition())

        while self.state == States.CONFIG:
            dt = self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT

                # Event resposible for protects minimum window size
                if event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.size
                    if self.isResolutionChanged():
                        if screen_width < Constants.MIN_SCREEN_WIDTH:
                            screen_width = Constants.MIN_SCREEN_WIDTH
                        if screen_height < Constants.MIN_SCREEN_HEIGHT:
                            screen_height = Constants.MIN_SCREEN_HEIGHT
                        Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = screen_width, screen_height
                        self.screen = pygame.display.set_mode(  size=(screen_width, screen_height), 
                                                                flags=pygame.RESIZABLE)
                        self.updateResolution()
                        self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
                        self.screen_surface = pygame.display.get_surface()
                        config_hud_container.set_position((0, Constants.SCREEN_HEIGHT-Constants.HUD_HEIGHT))
                        
                        config_hud_container_min_width = last_control.get_abs_rect()[0] + last_control.get_abs_rect()[2] + Constants.PADDING
                        config_hud_container.set_dimensions((config_hud_container_min_width, Constants.HUD_HEIGHT))
                        config_hud_container.set_position(((Constants.SCREEN_WIDTH - config_hud_container_min_width) // 2, Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 1 == event.button:
                        if True == self.start_point.getBoundingBox().collidepoint(pygame.mouse.get_pos()):
                            self.start_point.setMovable(state=True)
                        elif True == self.end_point.getBoundingBox().collidepoint(pygame.mouse.get_pos()):
                            self.end_point.setMovable(state=True)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if 1 == event.button:
                        self.start_point.setMovable(state=False)
                        self.end_point.setMovable(state=False)
                elif event.type == pygame.MOUSEMOTION:
                    if True == self.start_point.isMovable():
                        self.start_point.setPosition(pygame.mouse.get_pos())
                        self.trajectory.setOffset(self.start_point.getPosition())
                        self.trajectory.calculate()
                        self.end_point.updatePosition()
                    elif True == self.end_point.isMovable():
                        self.end_point.setPosition(pygame.mouse.get_pos())

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # Velocity
                    if event.ui_element == velocity_increase_button:
                        if self.trajectory.getVelocity() < Constants.VELOCITY_MAX:
                            self.trajectory.setVelocity(self.trajectory.getVelocity() + Constants.VELOCITY_STEP)
                            velocity_value_label.set_text(f"{self.trajectory.getVelocity()}")
                    if event.ui_element == velocity_decrease_button:
                        if self.trajectory.getVelocity() > 0:
                            self.trajectory.setVelocity(self.trajectory.getVelocity() - Constants.VELOCITY_STEP)
                            velocity_value_label.set_text(f"{self.trajectory.getVelocity()}")
                    # Angle
                    if event.ui_element == angle_increase_button:
                        if self.trajectory.getAngle() < Constants.ANGLE_MAX:
                            self.trajectory.setAngle(self.trajectory.getAngle() + Constants.ANGLE_STEP)
                        else:
                            self.trajectory.setAngle(0)
                        angle_value_label.set_text(f"{round(self.trajectory.getAngle(), 2)}")
                    if event.ui_element == angle_decrease_button:
                        if self.trajectory.getAngle() > 0:
                            self.trajectory.setAngle(self.trajectory.getAngle() - Constants.ANGLE_STEP)
                        else:
                            self.trajectory.setAngle(Constants.ANGLE_MAX)
                        angle_value_label.set_text(f"{round(self.trajectory.getAngle(), 2)}")
                    # Air Drag
                    if event.ui_element == air_drag_button:
                        if self.trajectory.isDrag() == True:
                            self.trajectory.setDrag(False)
                            air_drag_button.set_text("Enable")

                        else:
                            self.trajectory.setDrag(True)
                            air_drag_button.set_text("Disable")                        
                    # Start
                    if event.ui_element == start_button:
                        for control in controls:
                            control.kill()
                        self.state = States.SIMULATION
                    
                    self.trajectory.calculate()
                    self.end_point.updatePosition()
                
                self.manager.process_events(event)

            self.manager.update(dt)

            self.screen.fill(Constants.BLACK)

            self.trajectory.draw(surface=self.screen_surface, gap=Constants.CONFIG_TRAJECTORY_GAP)
            self.start_point.drawBBox(surface=self.screen_surface)
            self.start_point.draw(surface=self.screen_surface)
            self.end_point.drawBBox(surface=self.screen_surface)
            self.end_point.draw(surface=self.screen_surface)

            self.manager.draw_ui(window_surface=self.screen_surface)
     
            pygame.display.flip()

    def stateSIMULATION(self) -> None:
        print(f"{self.state.name = }")

        visbility_of_characteristic_points = True
        is_pause = False
        store_delta_x = 0
        simulation_speed_step = 1
        idx = 0

        self.trajectory.setDt(1e-3)
        self.trajectory.calculate()

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
                
                hud_container_min_width = last_control.get_abs_rect()[0] + last_control.get_abs_rect()[2] + Constants.PADDING
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

            idx += simulation_speed_step * dt
            self.clay.setPosition(self.trajectory.getPoint(idx))

            self.screen_surface.fill(Constants.BLACK)
            
            if True == visbility_of_characteristic_points:
                self.trajectory.draw(self.screen_surface, gap=Constants.SIMULATION_TRAJECTORY_GAP)
            self.start_point.draw(surface=self.screen_surface)
            self.end_point.draw(surface=self.screen_surface)
            self.clay.draw(surface=self.screen_surface)

            self.manager.draw_ui(window_surface=self.screen_surface)

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
        
    def run(self) -> None:
        self.stateMachine()