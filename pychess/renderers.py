import pygame
from pygame import gfxdraw

from .variables import cell_size, window_padding, board

green_dot_radius = int(cell_size / 4.5)
green_dot_color = (11, 218, 81)


def render_board(screen: pygame.display):
    screen.fill((10, 10, 10))

    for x in range(8):
        for y in range(8):
            color = (200, 200, 200) if (x + y) % 2 else (130, 130, 130)
            pygame.draw.rect(screen, color, (
                    y * cell_size + window_padding,
                    x * cell_size + window_padding,
                    cell_size,
                    cell_size,
                )
            )


def render_pieces(screen: pygame.display):
    for piece in board.pieces:
        piece.render(screen)


def render_choices(screen: pygame.display):
    for x in range(8):
        for y in range(8):
            if board.choices[x][y]:
                x_pos = int(x * cell_size + window_padding + cell_size / 2)
                y_pos = int(y * cell_size + window_padding + cell_size / 2)
                gfxdraw.aacircle(screen, x_pos, y_pos, green_dot_radius, green_dot_color)
                gfxdraw.filled_circle(screen, x_pos, y_pos, green_dot_radius, green_dot_color)
