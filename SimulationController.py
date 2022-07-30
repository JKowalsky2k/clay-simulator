import enum
import pygame
import CramerSolver
import SetupTrajectory
import Constants

class States(enum.Enum):
    CONFIG = 0
    SIMULATION = 1
    RESET = 2
    EXIT = 3

class SimulationController:
    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()
        self.FPS = 120

        self.screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), 
                                              pygame.RESIZABLE)
        self.screen = pygame.display.get_surface()
        Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()
        pygame.display.set_caption('Clay simulator v1.2')
       
        self.font = pygame.font.Font("fonts/basic.ttf", 16)
        self.trajectory = SetupTrajectory.Trajectory()
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
        stage = 1

        while self.state == States.CONFIG:
            Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if stage < 4:
                            stage += 1
                        elif stage == 4:
                            self.state = States.SIMULATION
            self.screen.fill(Constants.BLACK)

            config_text = self.font.render("Setup trajectory", 
                                True, 
                                Constants.WHITE, 
                                Constants.BLACK)
            config_text_rect = config_text.get_rect()
            config_text_rect.x, config_text_rect.y = Constants.SCREEN_WIDTH//2-config_text_rect.width/2, Constants.SCREEN_HEIGHT//15
            self.screen.blit(config_text, config_text_rect)

            if stage == 1:
                self.trajectory.setGroundLine(pygame.mouse.get_pos())
            elif stage == 2:
                self.trajectory.setStartClayPosition(pygame.mouse.get_pos())
            elif stage == 3:
                self.trajectory.setStopClayPosition(pygame.mouse.get_pos())
            elif stage == 4:
                self.trajectory.setApogeum(pygame.mouse.get_pos())
            
            if stage > 0:
                self.trajectory.drawGroundLine(self.screen)
            if stage > 1:
                self.trajectory.drawStartClayPosition(self.screen)
            if stage > 2:
                self.trajectory.drawStopClayPosition(self.screen)
            if stage > 3:
                self.trajectory.drawApogeum(self.screen)
            
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
        previous_delta_x = 0

        while self.state == States.SIMULATION:
            Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT

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
                        if delta_x < 10.0:
                            delta_x += 0.1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if round(delta_x, 2) > 0:
                            delta_x -= 0.1
                    elif event.key == pygame.K_RSHIFT:
                        if is_pause == True:
                            is_pause = False
                            delta_x = previous_delta_x
                        else:
                            is_pause = True
                            previous_delta_x = delta_x
                            delta_x = 0

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
            
            self.trajectory.drawGroundLine(self.screen)
            if visbility_of_characteristic_points == True:
                self.trajectory.drawStartClayPosition(self.screen)
                self.trajectory.drawStopClayPosition(self.screen)
                self.trajectory.drawApogeum(self.screen)

            pygame.draw.circle(surface=self.screen,
                               color=Constants.ORANGE,
                               center=self.translate(clay_position),
                               radius=flying_clay_radius)

            clay_position.x += delta_x

            if clay_position.x > self.trajectory.getStopClayPosition().x:
                clay_position = self.translate(self.trajectory.getStartClayPosition())

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