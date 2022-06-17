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

        self.screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self.screen = pygame.display.get_surface()
        self.screen.blit(pygame.transform.flip(self.screen, False, True), dest=(0, 0))

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
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if stage == 1:
                            stage = 2
                        elif stage == 2:
                            stage = 3
                        elif stage == 3:
                            stage = 4
                        elif stage == 4:
                            self.state = States.SIMULATION
                    elif event.button == 3:
                        print("RIGHT")
            self.screen.fill(Constants.BLACK)

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
        print(f"{clay_position = }")

        while self.state == States.SIMULATION:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
            self.screen.fill(Constants.BLACK)

            if clay_position.x <= self.trajectory.getApogeum().x:
                clay_position.y = parabole1["a"]*clay_position.x**2+parabole1["b"]*clay_position.x+parabole1["c"]
            elif clay_position.x > self.trajectory.getApogeum().x:
                clay_position.y = parabole2["a"]*clay_position.x**2+parabole2["b"]*clay_position.x+parabole2["c"]
            
            #print("after_mods:", f"{clay_position = }")

            self.trajectory.drawGroundLine(self.screen)
            self.trajectory.drawStartClayPosition(self.screen)
            self.trajectory.drawStopClayPosition(self.screen)
            self.trajectory.drawApogeum(self.screen)

            pygame.draw.circle(surface=self.screen,
                               color=Constants.ORANGE,
                               center=self.translate(clay_position),
                               radius=Constants.CLAY_RADIUS)

            clay_position.x += 0.8

            if clay_position.x > self.trajectory.getStopClayPosition().x:
                self.state = States.CONFIG

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