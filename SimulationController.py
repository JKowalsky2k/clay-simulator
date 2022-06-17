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

        solver = CramerSolver.CramerSolver(pygame.math.Vector2(-2, 0), pygame.math.Vector2(4, 0), pygame.math.Vector2(1, 5))
        print(solver.result())

        trajectory = SetupTrajectory.Trajectory()

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
                trajectory.setGroundLine(pygame.mouse.get_pos())
            elif stage == 2:
                trajectory.setStartClayPosition(pygame.mouse.get_pos())
            elif stage == 3:
                trajectory.setStopClayPosition(pygame.mouse.get_pos())
            elif stage == 4:
                trajectory.setApogeum(pygame.mouse.get_pos())

            trajectory.drawGroundLine(self.screen)
            if stage > 1:
                trajectory.drawStartClayPosition(self.screen)
            if stage > 2:
                trajectory.drawStopClayPosition(self.screen)
            if stage > 3:
                trajectory.drawApogeum(self.screen)
            
            pygame.display.flip()

    def stateSIMULATION(self) -> None:
        print(f"{self.state.name = }")
        while self.state == States.SIMULATION:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT

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