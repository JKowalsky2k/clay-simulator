from ast import Constant
import enum

class ConfigStates(enum.Enum):
    START = 0
    STOP = 1
    APOGEUM = 2

a = ConfigStates.START
print(a.value)

# import pygame
# import pygame_gui


# pygame.init()

# pygame.display.set_caption('Quick Start')
# window_surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

# background = pygame.Surface((800, 600))
# background.fill(pygame.Color('#000000'))

# manager = pygame_gui.UIManager((800, 600))
# manager.set_visual_debug_mode(True)

# # hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
# #                                             text='Say Hello',
# #                                             manager=manager)

# container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect(0, 0, 800, 600),
#                             manager=manager,
#                             starting_height=0)

# print(container.get_rect()[2]//2, container.get_rect()[3]//2)
# button_layout_rect = pygame.Rect(container.get_rect()[2]//2, container.get_rect()[3]//2, 100, 50)
# # button_layout_rect.center = (0, 0)

# hello_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
#                                             text='Hello', manager=manager,
#                                             container=container,
#                                             anchors={'left': 'left',
#                                                 'right': 'left',
#                                                 'top': 'top',
#                                                 'bottom': 'top'})

# clock = pygame.time.Clock()
# is_running = True

# while is_running:
#     time_delta = clock.tick(60)/1000.0
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             is_running = False

#         if event.type == pygame_gui.UI_BUTTON_PRESSED:
#             if event.ui_element == hello_button:
#                 print(container.get_rect())

#         manager.process_events(event)

#     manager.update(time_delta)

#     window_surface.blit(background, (0, 0))
#     manager.draw_ui(window_surface)

#     pygame.display.update()