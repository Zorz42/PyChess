import pygame
from pychess.util import is_occupied

window_padding = 10
cell_size = 16
scale = 3

window_size = (cell_size * 8 + window_padding * 2) * scale


def init():
    pygame.init()
    pygame.display.set_caption('PyChess')

    screen = pygame.display.set_mode((window_size, window_size))

    return screen


def handle(event: pygame.event):
    # Handle event(s)
    pass


def render(screen: pygame.display):
    # Render to screen?
    screen.fill((10, 10, 10))
    for x in range(8):
        for y in range(8):
            color = (200, 200, 200) if (x + y) % 2 else (130, 130, 130)
            pygame.draw.rect(screen, color, ((x * cell_size + window_padding) * scale,
                                             (y * cell_size + window_padding) * scale,
                                             cell_size * scale,
                                             cell_size * scale,
                                             )
                             )
    pygame.display.flip()
