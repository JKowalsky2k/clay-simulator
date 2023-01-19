from tracemalloc import start
import pygame
import pygame_gui
import enum
import Trajectory
import SimulationSettings
import Constants
import Point
import StartPoint
import House
import EndPoint
import BackgroundController
import ConfigControlsController
import SimulationControlsController
import SecurityController

class States(enum.Enum):
    CONFIG = 0
    SIMULATION = 1
    RESET = 2
    EXIT = 3

class SimulationController(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.init()
        pygame.sprite.Sprite.__init__(self)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.screen = pygame.display.set_mode(size=(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), 
                                              flags=pygame.RESIZABLE)
        self.screen_surface = pygame.display.get_surface()
        Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()

        self.manager = pygame_gui.UIManager(window_resolution=(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), 
                                            theme_path="themes/theme.json")
    
        pygame.display.set_caption('Clay simulator (ver. 17.09.2022)')

        self.security = SecurityController.Security()
       
        self.trajectory = Trajectory.Trajectory()
        self.state = States.CONFIG

        self.backgorund = BackgroundController.BackgorundController(path="./images/backgrounds")

        # self.start_point = StartPoint.StartPoint( position=(Constants.SCREEN_WIDTH//3, Constants.SCREEN_HEIGHT/2), 
        #                                           radius=SimulationSettings.CLAY_SIZE,
        #                                           color=Constants.RED,
        #                                           trajectory=self.trajectory)
        self.start_point = House.House( position=(Constants.SCREEN_WIDTH // 2 , Constants.SCREEN_HEIGHT // 2),
                                        width=40,
                                        height=80,
                                        color=Constants.BROWN,
                                        trajectory=self.trajectory)
        self.end_point = EndPoint.EndPoint( position=(0, 0), 
                                            radius=SimulationSettings.CLAY_SIZE,
                                            color=Constants.BLUE,
                                            trajectory=self.trajectory)
        self.clay = Point.Point(position=(0, 0), 
                                radius=SimulationSettings.CLAY_SIZE,
                                color=Constants.ORANGE,
                                trajectory=self.trajectory)

        self.configGUI = ConfigControlsController.ConfigGUI(manager=self.manager, trajectory=self.trajectory, background=self.backgorund)
        self.simulationGUI = SimulationControlsController.SimulationGUI(manager=self.manager, trajectory=self.trajectory, background=self.backgorund, clay=self.clay)

        self.trajectory.setDt(1e-2)
        self.trajectory.setOffset(self.start_point.getPosition())
        self.trajectory.calculate()
        self.end_point.setPosition(self.trajectory.getLastPointPosition())

    def updateResolution(self):
        Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = self.screen.get_size()

    def isResolutionChanged(self):
        return True if self.screen.get_size() != (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT) else False

    def stateMachine(self) -> None:
        if True == self.security.check():
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

        self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self.configGUI.create()
        self.configGUI.updateContainer()

        self.trajectory.setDt(1e-2)
        self.trajectory.setOffset(self.start_point.getPosition())
        self.trajectory.calculate()

        while self.state == States.CONFIG:
            dt = self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = States.EXIT

                # Event resposible for protects minimum window size
                if event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.size
                    if True == self.isResolutionChanged():
                        if screen_width < Constants.MIN_SCREEN_WIDTH:
                            screen_width = Constants.MIN_SCREEN_WIDTH
                        if screen_height < Constants.MIN_SCREEN_HEIGHT:
                            screen_height = Constants.MIN_SCREEN_HEIGHT
                        Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = screen_width, screen_height
                        Constants.BOTTOM_EDGE_OF_SCRREN_SURFACE = Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT
                        self.screen = pygame.display.set_mode(  size=(screen_width, screen_height), 
                                                                flags=pygame.RESIZABLE)
                        self.updateResolution()
                        self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
                        self.screen_surface = pygame.display.get_surface()
                        self.configGUI.updateContainer()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 1 == event.button:
                        if True == self.end_point.getBoundingBox().collidepoint(pygame.mouse.get_pos()):
                            self.end_point.setMovable(state=True)
                        elif True == self.start_point.getBoundingBox().collidepoint(pygame.mouse.get_pos()):
                            self.start_point.setMovable(state=True)
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
                
                status = self.configGUI.event(event=event)
                if status == False:
                    self.trajectory.calculate()
                    self.end_point.updatePosition()
                elif status == True:
                    self.state = States.SIMULATION
                
                self.manager.process_events(event)

            self.manager.update(dt)

            self.backgorund.draw(surface=self.screen_surface)

            self.trajectory.drawAll(surface=self.screen_surface)
            self.start_point.draw(surface=self.screen_surface)
            self.end_point.draw(surface=self.screen_surface)

            hud_background = pygame.Surface((Constants.SCREEN_WIDTH, Constants.HUD_HEIGHT))
            hud_background.fill(Constants.BLACK)
            self.screen_surface.blit(hud_background, (0, Constants.BOTTOM_EDGE_OF_SCRREN_SURFACE))
            self.manager.draw_ui(window_surface=self.screen_surface)
     
            pygame.display.flip()

    def stateSIMULATION(self) -> None:
        print(f"{self.state.name = }")

        SimulationSettings.INDEX = 0
        start_mode = False

        self.trajectory.setDt(new_dt=0.0025)
        self.trajectory.calculate()
        self.end_point.fixPosition()
        self.trajectory.setEndIndex(end_index=self.trajectory.getIndex(self.end_point.getPosition()))

        self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self.simulationGUI.create()
        self.simulationGUI.updateContainer()
        
        while self.state == States.SIMULATION:
            dt = self.clock.tick(self.FPS)

            if self.isResolutionChanged():
                if screen_width < Constants.MIN_SCREEN_WIDTH:
                    screen_width = Constants.MIN_SCREEN_WIDTH
                if screen_height < Constants.MIN_SCREEN_HEIGHT:
                    screen_height = Constants.MIN_SCREEN_HEIGHT
                Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT = screen_width, screen_height
                Constants.BOTTOM_EDGE_OF_SCRREN_SURFACE = Constants.SCREEN_HEIGHT - Constants.HUD_HEIGHT
                self.screen = pygame.display.set_mode(  size=(screen_width, screen_height), 
                                                        flags=pygame.RESIZABLE)
                self.updateResolution()
                self.manager.set_window_resolution((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
                self.screen_surface = pygame.display.get_surface()
                self.simulationGUI.updateContainer()

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
                    if event.key == pygame.K_SPACE:
                        start_mode = True

                state = self.simulationGUI.event(event)
                if True == state:
                    self.state = States.CONFIG

                self.manager.process_events(event)

            self.manager.update(dt)

            if SimulationSettings.START_MODE == "Auto":
                start_mode = True

            if True == start_mode:
                SimulationSettings.INDEX += SimulationSettings.SPEED * dt
                if SimulationSettings.INDEX > self.trajectory.getEndIndex():
                    SimulationSettings.INDEX = 0
                    if SimulationSettings.START_MODE == "Manual":
                        start_mode = False
            self.clay.setPosition(self.trajectory.getPoint(SimulationSettings.INDEX))
            
            self.backgorund.draw(surface=self.screen_surface)

            if True == SimulationSettings.VISIBILITY:
                self.trajectory.draw(self.screen_surface)
                self.end_point.draw(surface=self.screen_surface)
            self.clay.drawSprite(surface=self.screen_surface)
            self.start_point.draw(surface=self.screen_surface)

            hud_background = pygame.Surface((Constants.SCREEN_WIDTH, Constants.HUD_HEIGHT))
            hud_background.fill(Constants.BLACK)
            self.screen_surface.blit(hud_background, (0, Constants.BOTTOM_EDGE_OF_SCRREN_SURFACE))
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