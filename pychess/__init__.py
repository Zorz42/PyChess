import pygame
from pygame import gfxdraw
from numpy import full

from .renderers import render_board, render_pieces, render_choices
from .util import is_occupied, get_piece
from .variables import cell_size, window_padding, board

green_dot_radius = int(cell_size / 4.5)
green_dot_color = (11, 218, 81)


def init():
    pygame.init()
    pygame.display.set_caption('PyChess')

    window_size = cell_size * 8 + window_padding * 2
    screen = pygame.display.set_mode((window_size, window_size))

    # Test: Create piece
    from .pieces import King
    board.pieces.append(King(0, 0, False))
    board.pieces.append(King(3, 2, True))
    board.pieces.append(King(0, 5, False))

    return screen


def handle(event: pygame.event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = int((mouse_x - window_padding) / cell_size)
        mouse_y = int((mouse_y - window_padding) / cell_size)

        piece = get_piece(mouse_x, mouse_y)
        board.choices = full((0, 0), False) if piece is None else piece.scan_board()


def render_bool_board(screen: pygame.display):
    if board.size:
        for x in range(8):
            for y in range(8):
                if board[x][y]:
                    x_pos = int(x * cell_size + window_padding + cell_size / 2)
                    y_pos = int(y * cell_size + window_padding + cell_size / 2)
                    gfxdraw.aacircle(screen, x_pos, y_pos, green_dot_radius, green_dot_color)
                    gfxdraw.filled_circle(screen, x_pos, y_pos, green_dot_radius, green_dot_color)


def render(screen: pygame.display):
    render_board(screen, cell_size, window_padding)
    render_pieces(screen)
    render_choices(screen)

    pygame.display.flip()
