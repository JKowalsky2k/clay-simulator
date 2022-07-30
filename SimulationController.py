import enum
import pygame
import pygame_gui
import CramerSolver
import SetupTrajectory
import Constants

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

        self.manager = pygame_gui.UIManager((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self.hud_height = 100
        
        pygame.display.set_caption('Clay simulator v1.2')
       
        self.font = pygame.font.Font("fonts/basic.ttf", 16)
        self.trajectory = SetupTrajectory.Trajectory(self.screen, self.hud_height)
        self.state = States.CONFIG

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
            Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
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
            hud_area.fill((255, 255, 0, 96))
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
        
        delta_x = 0.8
        flying_clay_radius = Constants.CLAY_RADIUS
        visbility_of_characteristic_points = True
        is_pause = False
        direction = "Right"
        store_delta_x = 0

        hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                                    text='Say Hello',
                                                    manager=self.manager)

        while self.state == States.SIMULATION:
            Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()
            dt = self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == hello_button:
                        print('Hello World!')
                
                self.manager.process_events(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = States.EXIT
                    elif event.key == pygame.K_RETURN:
                        self.state = States.CONFIG
                    elif event.key == pygame.K_SPACE:
                        if visbility_of_characteristic_points == True:
                            visbility_of_characteristic_points = False
                        else:
                            visbility_of_characteristic_points = True
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if flying_clay_radius < 40:
                            flying_clay_radius += 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if flying_clay_radius > 2:
                            flying_clay_radius -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if delta_x < 2.0:
                            delta_x += 0.05
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if round(delta_x, 2) > 0:
                            delta_x -= 0.05
                    elif event.key == pygame.K_RSHIFT:
                        if is_pause == True:
                            is_pause = False
                            delta_x = store_delta_x
                        else:
                            is_pause = True
                            store_delta_x = delta_x
                            delta_x = 0
                    elif event.key == pygame.K_LSHIFT:
                        if direction == "Right":
                            direction = "Left"
                        else:
                            direction = "Right"
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == hello_button:
                            print('Hello World!')

            self.manager.update(dt)

            self.screen.fill(Constants.BLACK)

            delta_x_text = self.font.render("Velocity: {}".format(round(delta_x, 2)), 
                                True, 
                                Constants.WHITE, 
                                Constants.BLACK)
            delta_x_text_rect = delta_x_text.get_rect()
            delta_x_text_rect.x, delta_x_text_rect.y = 0, 0
            self.screen.blit(delta_x_text, delta_x_text_rect)

            if clay_position.x <= self.trajectory.getApogeum().x:
                clay_position.y = parabole1["a"]*clay_position.x**2+parabole1["b"]*clay_position.x+parabole1["c"]
            elif clay_position.x > self.trajectory.getApogeum().x:
                clay_position.y = parabole2["a"]*clay_position.x**2+parabole2["b"]*clay_position.x+parabole2["c"]
            
            # self.trajectory.drawGroundLine(self.screen)
            if visbility_of_characteristic_points == True:
                self.trajectory.drawStartClayPosition()
                self.trajectory.drawStopClayPosition()
                self.trajectory.drawApogeum()

            pygame.draw.circle(surface=self.screen,
                               color=Constants.ORANGE,
                               center=self.translate(clay_position),
                               radius=flying_clay_radius)

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
    
    def translateToPixel(self, vector) -> tuple:
        v = pygame.math.Vector2(vector.x, Constants.SCREEN_HEIGHT - vector.y)
        return (int(v.x), int(v.y))

    def run(self) -> None:
        self.stateMachine()