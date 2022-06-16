import pygame as pg
from SimulationController import SimulationController

def init():
    pg.init()
    global screen
    screen = pg.display.set_mode([500, 500])

def main_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return

        screen.fill((255, 255, 255))

        pg.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        screen.set_at((100, 100), (0, 0, 0))

        pg.display.flip()

sim = SimulationController()
sim.run()

