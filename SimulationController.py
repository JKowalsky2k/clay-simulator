import enum
import pygame
import pygame_gui
import CramerSolver
import SetupTrajectory
import Constants
import numpy as np 
import math 
import scipy.constants as const 

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
        self.hud_height = 100
        pygame.display.set_caption('Clay simulator (ver. 30.07.2022)')
       
        self.font = pygame.font.Font("fonts/basic.ttf", 16)
        self.trajectory = SetupTrajectory.Trajectory(self.screen, self.hud_height)
        self.state = States.CONFIG


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
        
        config_stage_counter = 1
        number_of_stages = len(["SET_START_POS", "SET_STOP_POS", "SET_APOGEUM_POS"])

        config_text = self.font.render("Setup trajectory", 
                                        True, 
                                        Constants.WHITE, 
                                        Constants.BLACK)

        while self.state == States.CONFIG:
            self.clock.tick(self.FPS)
            if self.isResolutionChanged():
                self.updateResolution()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
                # Event resposible for protects minimum widow size
                elif event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.size
                    if screen_width < Constants.MIN_SCREEN_WIDTH:
                        screen_width = Constants.MIN_SCREEN_WIDTH
                    if screen_height < Constants.MIN_SCREEN_HEIGHT:
                        screen_height = Constants.MIN_SCREEN_HEIGHT
                    self.screen = pygame.display.set_mode(  size=(screen_width, screen_height), 
                                                            flags=pygame.RESIZABLE)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if config_stage_counter < number_of_stages:
                            config_stage_counter += 1
                        elif config_stage_counter == number_of_stages:
                            self.state = States.SIMULATION

            self.screen.fill(Constants.BLACK)

            config_text_rect = config_text.get_rect()
            config_text_rect.x, config_text_rect.y = Constants.SCREEN_WIDTH//2-config_text_rect.width/2, Constants.SCREEN_HEIGHT//15
            self.screen.blit(config_text, config_text_rect)

            hud_area = pygame.Surface((Constants.SCREEN_WIDTH, self.hud_height), pygame.SRCALPHA)
            # Color: yellow, Alpha: 96
            hud_area.fill((255, 255, 0, 150))
            self.screen.blit(hud_area, self.translateToPixel(pygame.math.Vector2(0, self.hud_height)))

            if config_stage_counter == 1:
                self.trajectory.setStartClayPosition(pygame.mouse.get_pos())
            elif config_stage_counter == 2:
                self.trajectory.setStopClayPosition(pygame.mouse.get_pos())
            elif config_stage_counter == 3:
                self.trajectory.setApogeum(pygame.mouse.get_pos())
            
            if config_stage_counter > 0:
                self.trajectory.drawStartClayPosition()
            if config_stage_counter > 1:
                self.trajectory.drawStopClayPosition()
            if config_stage_counter > 2:
                self.trajectory.drawApogeum()
            
            pygame.display.flip()

    def stateSIMULATION(self) -> None:
        print(f"{self.state.name = }")

        P1_left = self.translate(self.trajectory.getStartClayPosition())
        P1_center = self.translate(self.trajectory.getApogeum())
        P1_right = pygame.math.Vector2(P1_left.x + 2*(P1_center.x-P1_left.x), P1_left.y)

        P2_center = self.translate(self.trajectory.getApogeum())
        P2_right = self.translate(self.trajectory.getStopClayPosition())
        P2_left = pygame.math.Vector2(P2_right.x - 2*(P2_right.x-P2_center.x), P2_right.y)

        parabole1 = CramerSolver.CramerSolver(P1_left,
                                             P1_right, 
                                             P1_center).result()

        parabole2 = CramerSolver.CramerSolver(P2_left,
                                             P2_right, 
                                             P2_center).result()


        clay_position = self.translate(self.trajectory.getStartClayPosition())
        
        delta_x = 0.1
        clay_size = Constants.CLAY_RADIUS
        visbility_of_characteristic_points = True
        is_pause = False
        direction = "Right"
        store_delta_x = 0
        angle = math.pi/4
        v = 40

        controls = []

        self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        hud_container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect(0, Constants.SCREEN_HEIGHT-self.hud_height, Constants.SCREEN_WIDTH, self.hud_height),
                                                    container=self.manager.get_root_container(),
                                                    manager=self.manager)
        controls.append(hud_container)

        # Section HUD Velocity

        velocity_name_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(10, 10, 90, 20),
                                                            text='Velocity', 
                                                            manager=self.manager,
                                                            container=hud_container)
        controls.append(velocity_name_label)

        velocity_value_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(10, 40, 90, 20),
                                                            text=f"{delta_x}", 
                                                            manager=self.manager,
                                                            container=hud_container)
        controls.append(velocity_value_label)
        
        velocity_increase_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(10, 70, 40, 20),
                                                                text='+', 
                                                                manager=self.manager,
                                                                container=hud_container)
        controls.append(velocity_increase_button)
        
        velocity_decrease_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(60, 70, 40, 20),
                                                                text='-', 
                                                                manager=self.manager,
                                                                container=hud_container)
        controls.append(velocity_decrease_button)

        # Section HUD Clay size

        size_name_label = pygame_gui.elements.UILabel(  relative_rect=pygame.Rect(110, 10, 90, 20),
                                                        text='Size', 
                                                        manager=self.manager,
                                                        container=hud_container)
        controls.append(size_name_label)

        size_value_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(110, 40, 90, 20),
                                                        text=f"{clay_size}", 
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
        
        # Section HUD Direction

        direction_name_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(210, 10, 90, 20),
                                                            text='Direction', 
                                                            manager=self.manager,
                                                            container=hud_container)
        controls.append(direction_name_label)
        
        direction_left_button = pygame_gui.elements.UIButton(   relative_rect=pygame.Rect(210, 40, 90, 20),
                                                                text='<', 
                                                                manager=self.manager,
                                                                container=hud_container)
        controls.append(direction_left_button)
        
        direction_right_button = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(210, 70, 90, 20),
                                                                text='>', 
                                                                manager=self.manager,
                                                                container=hud_container)
        controls.append(direction_right_button)

        if direction == "Right":
            direction_right_button.disable()
        else:
            direction_left_button.disable()

        # Section HUD Visibility

        visibility_name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(310, 10, 90, 20),
                                                            text='Visibility', 
                                                            manager=self.manager,
                                                            container=hud_container)
        controls.append(visibility_name_label)

        visibility_button = pygame_gui.elements.UIButton(   relative_rect=pygame.Rect(310, 40, 90, 50),
                                                            text='Disable', 
                                                            manager=self.manager,
                                                            container=hud_container)
        controls.append(visibility_button)

        # Section HUD Pause

        pause_name_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(410, 10, 90, 20),
                                                        text='Pause', 
                                                        manager=self.manager,
                                                        container=hud_container)
        controls.append(pause_name_label)

        pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(410, 40, 90, 50),
                                                    text='Enable', 
                                                    manager=self.manager,
                                                    container=hud_container)
        controls.append(pause_button)

        # Section HUD Trajectory Selection

        trajectory_selection_label = pygame_gui.elements.UILabel( relative_rect=pygame.Rect(510, 10, 260, 20),
                                                                  text='Trajectory', 
                                                                  manager=self.manager,
                                                                  container=hud_container)
        controls.append(trajectory_selection_label)                                                                    

        trajectory_1_selection = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(510, 40, 50, 50),
                                                                text='1', 
                                                                manager=self.manager,
                                                                container=hud_container,
                                                                object_id=pygame_gui.core.ObjectID(object_id="#trajectory_button"))
        controls.append(trajectory_1_selection)

        trajectory_2_selection = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(580, 40, 50, 50),
                                                                text='2', 
                                                                manager=self.manager,
                                                                container=hud_container,
                                                                object_id=pygame_gui.core.ObjectID(object_id="#trajectory_button"))
        controls.append(trajectory_2_selection)

        trajectory_3_selection = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(650, 40, 50, 50),
                                                                text='3', 
                                                                manager=self.manager,
                                                                container=hud_container,
                                                                object_id=pygame_gui.core.ObjectID(object_id="#trajectory_button"))
        controls.append(trajectory_3_selection)
        
        trajectory_4_selection = pygame_gui.elements.UIButton(  relative_rect=pygame.Rect(720, 40, 50, 50),
                                                                text='4', 
                                                                manager=self.manager,
                                                                container=hud_container,
                                                                object_id=pygame_gui.core.ObjectID(object_id="#trajectory_button"))
        controls.append(trajectory_4_selection)

        # Section HUD Reset

        last_control = reset_button = pygame_gui.elements.UIButton( relative_rect=pygame.Rect(780, 10, 90, 80),
                                                                    text='Reset', 
                                                                    manager=self.manager,
                                                                    container=hud_container)
        controls.append(reset_button)

        right_padding = 10
        hud_container_min_width = last_control.get_abs_rect()[0] + last_control.get_abs_rect()[2] + right_padding
        hud_container.set_dimensions((hud_container_min_width, self.hud_height))
        hud_container.set_position(((Constants.SCREEN_WIDTH - hud_container_min_width) // 2, Constants.SCREEN_HEIGHT - self.hud_height))

        update_clay = pygame.USEREVENT
        pygame.time.set_timer(update_clay, 1)
        idx = 0

        points = self.trajectory.projectile_motion(angle=angle, v0=v)
        
        while self.state == States.SIMULATION:
            dt = self.clock.tick(self.FPS)
            if self.isResolutionChanged():
                self.updateResolution()
                self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
                hud_container.set_position((0, Constants.SCREEN_HEIGHT-self.hud_height))
                
                P1_left = self.translate(self.trajectory.getStartClayPosition())
                P1_center = self.translate(self.trajectory.getApogeum())
                P1_right = pygame.math.Vector2(P1_left.x + 2*(P1_center.x-P1_left.x), P1_left.y)

                P2_center = self.translate(self.trajectory.getApogeum())
                P2_right = self.translate(self.trajectory.getStopClayPosition())
                P2_left = pygame.math.Vector2(P2_right.x - 2*(P2_right.x-P2_center.x), P2_right.y)

                parabole1 = CramerSolver.CramerSolver(P1_left,
                                                    P1_right, 
                                                    P1_center).result()

                parabole2 = CramerSolver.CramerSolver(P2_left,
                                                    P2_right, 
                                                    P2_center).result()
                
                right_padding = 10
                hud_container_min_width = last_control.get_abs_rect()[0] + last_control.get_abs_rect()[2] + right_padding
                hud_container.set_dimensions((hud_container_min_width, self.hud_height))
                hud_container.set_position(((Constants.SCREEN_WIDTH - hud_container_min_width) // 2, Constants.SCREEN_HEIGHT - self.hud_height))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
                # Event resposible for protects minimum widow size
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

                if event.type == update_clay:
                    # print(f'{idx = }')
                    if idx < len(points)-1:
                        idx += 1
                    else:
                        idx = 0

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # Velocity
                    if event.ui_element == velocity_increase_button:
                        if delta_x < 2.0:
                            delta_x += 0.05
                            delta_x = round(delta_x, 2)
                            pause_button.enable()
                            velocity_value_label.set_text(f"{round(delta_x, 2)}")
                            v += 1
                            print(f'{v = }')
                            points = self.trajectory.projectile_motion(angle=angle, v0=v)
                    if event.ui_element == velocity_decrease_button:
                        if delta_x > 0:
                            delta_x -= 0.05
                            delta_x = round(delta_x, 2)
                            if delta_x == 0:
                                pause_button.disable()
                            velocity_value_label.set_text(f"{round(delta_x, 2)}")
                        v -= 1
                        print(f'{v = }')
                        points = self.trajectory.projectile_motion(angle=angle, v0=v)
                    # Size
                    if event.ui_element == size_increase_button:
                        if clay_size < 40:
                            clay_size += 1
                            size_value_label.set_text(f"{round(clay_size, 2)}")
                            angle += math.pi/12
                            print(f'{angle = }')
                            points = self.trajectory.projectile_motion(angle=angle, v0=v)
                    if event.ui_element == size_decrease_button:
                        if clay_size > 2:
                            clay_size -= 1
                            size_value_label.set_text(f"{round(clay_size, 2)}")
                            angle -= math.pi/12
                            print(f'{angle = }')
                            points = self.trajectory.projectile_motion(angle=angle, v0=v)
                    # Direction
                    if event.ui_element == direction_left_button:
                        if direction == "Right":
                           direction = "Left"
                           direction_left_button.disable()
                           direction_right_button.enable()
                    if event.ui_element == direction_right_button:
                        if direction == "Left":
                           direction = "Right"
                           direction_right_button.disable()
                           direction_left_button.enable()
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
                            velocity_increase_button.enable()
                            velocity_decrease_button.enable()
                            delta_x = store_delta_x
                        else:
                            is_pause = True
                            store_delta_x = delta_x
                            delta_x = 0
                            pause_button.set_text("Disable")
                            velocity_increase_button.disable()
                            velocity_decrease_button.disable()
                        velocity_value_label.set_text(f"{round(delta_x, 2)}")
                    # Reset
                    if event.ui_element == reset_button:
                        self.state = States.CONFIG
                        for control in controls:
                            control.kill()
                        print(f"Killed all controls: {len(controls)}")                            

                self.manager.process_events(event)

            self.manager.update(dt)

            self.screen.fill(Constants.BLACK)

            if clay_position.x <= self.trajectory.getApogeum().x:
                clay_position.y = parabole1["a"]*clay_position.x**2+parabole1["b"]*clay_position.x+parabole1["c"]
            elif clay_position.x > self.trajectory.getApogeum().x:
                clay_position.y = parabole2["a"]*clay_position.x**2+parabole2["b"]*clay_position.x+parabole2["c"]
            
            if visbility_of_characteristic_points == True:
                self.trajectory.drawStartClayPosition()
                self.trajectory.drawStopClayPosition()
                self.trajectory.drawApogeum()

            pygame.draw.circle(surface=self.screen,
                               color=Constants.ORANGE,
                               center=self.translate(clay_position),
                               radius=clay_size)
            try:
                pygame.draw.circle(surface=self.screen,
                                color=Constants.ORANGE,
                                center=points[idx],
                                radius=clay_size)
            except:
                print(f'Error: {idx = }')
                print(f'{len(points) = }')
                exit(0)

            if direction == "Right":
                clay_position.x += delta_x * dt
            else:
                clay_position.x -= delta_x * dt

            if direction == "Right":
                if clay_position.x > self.trajectory.getStopClayPosition().x:
                    clay_position = self.translate(self.trajectory.getStartClayPosition())
            else:
                if clay_position.x < self.trajectory.getStartClayPosition().x:
                    clay_position = self.translate(self.trajectory.getStopClayPosition())
            
            for point in points:
                pygame.draw.circle(self.screen_surface, Constants.WHITE, point, 1)

            self.manager.draw_ui(self.screen)

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