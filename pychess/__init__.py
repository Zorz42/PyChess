import pygame
from pychess.util import is_occupied, render_board

cell_size = 48
window_padding = 30

window_size = cell_size * 8 + window_padding * 2


def init():
    pygame.init()
    pygame.display.set_caption('PyChess')

    screen = pygame.display.set_mode((window_size, window_size))

    return screen


def handle(event: pygame.event):
    # Handle event(s)
    pass


def render(screen: pygame.display):
    render_board(screen, cell_size, window_padding)
    # render_pieces(screen, board?)

    pygame.display.flip()
