import pygame
from .util import is_occupied, render_board, render_pieces

cell_size = 64
window_padding = 40

window_size = cell_size * 8 + window_padding * 2


def init():
    pygame.init()
    pygame.display.set_caption('PyChess')

    screen = pygame.display.set_mode((window_size, window_size))

    # Test: Create piece
    from .pieces import board, King
    board.append(King(0, 0, False))

    return screen


def handle(event: pygame.event):
    # Handle event(s)
    pass


def render(screen: pygame.display):
    render_board(screen, cell_size, window_padding)
    render_pieces(screen)

    pygame.display.flip()
