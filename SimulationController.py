import enum
import pygame

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
        self.FPS = 60

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

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
        while self.state == States.CONFIG:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT
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