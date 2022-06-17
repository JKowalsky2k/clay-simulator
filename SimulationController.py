import enum
import pygame
import CramerSolver
import SetupTrajectory

class States(enum.Enum):
    CONFIG = 0
    SIMULATION = 1
    RESET = 2
    EXIT = 3

class SimulationController:
    def __init__(self) -> None:
        pygame.init()
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500

        self.clock = pygame.time.Clock()
        self.FPS = 120

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.ORANGE = (255, 165,   0)
        self.RED    = (255,   0,   0)
        self.WHITE  = (255, 255, 255)
        self.BLACK  = (  0,   0,   0)

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

        while self.state == States.CONFIG:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("LEFT")
                    elif event.button == 3:
                        print("RIGHT")
            self.screen.fill(self.BLACK)

            trajectory.setGroundLine(pygame.mouse.get_pos())
            trajectory.drawGroundLine(self.screen)
            pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
            self.screen.set_at(self.translateToPixel(pygame.math.Vector2(100, 100)), (255, 255, 255))
            
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
        return pygame.math.Vector2(vector.x, self.SCREEN_HEIGHT - vector.y)
    
    def translateToPixel(self, vector) -> tuple:
        v = pygame.math.Vector2(vector.x, self.SCREEN_HEIGHT - vector.y)
        return (int(v.x), int(v.y))

    def run(self) -> None:
        self.stateMachine()