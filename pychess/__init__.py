import pygame
from pygame import gfxdraw
from numpy import full
from .util import is_occupied, render_board, render_pieces, get_piece
from .variables import cell_size, window_padding

bool_board = full([], False)

green_dot_radius = int(cell_size / 4.5)
green_dot_color = (11, 218, 81)


def init():
    pygame.init()
    pygame.display.set_caption('PyChess')

    window_size = cell_size * 8 + window_padding * 2
    screen = pygame.display.set_mode((window_size, window_size))

    # Test: Create piece
    from .pieces import board, King
    board.append(King(0, 0, False))
    board.append(King(3, 2, True))
    board.append(King(0, 5, False))

    return screen


def handle(event: pygame.event):
    # Handle event(s)
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = int((mouse_x - window_padding) / cell_size)
        mouse_y = int((mouse_y - window_padding) / cell_size)
        global bool_board
        piece = get_piece(mouse_x, mouse_y)
        if piece is None:
            bool_board = full([], False)
        else:
            bool_board = piece.scan_board()


def render_bool_board(screen: pygame.display):
    if bool_board.size != 1:
        for x in range(8):
            for y in range(8):
                if bool_board[x][y]:
                    x_pos = int(x * cell_size + window_padding + cell_size / 2)
                    y_pos = int(y * cell_size + window_padding + cell_size / 2)
                    gfxdraw.aacircle(screen, x_pos, y_pos, green_dot_radius, green_dot_color)
                    gfxdraw.filled_circle(screen, x_pos, y_pos, green_dot_radius, green_dot_color)


def render(screen: pygame.display):
    render_board(screen, cell_size, window_padding)
    render_pieces(screen)
    render_bool_board(screen)

    pygame.display.flip()
