import pygame
from pygame import gfxdraw

from .util import get_piece
from .variables import cell_size, window_padding, board

green_dot_radius = int(cell_size / 4.5)
green_dot_color = (11, 218, 81)
green_dot_color_hover = (8, 163, 61)


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
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x = int((mouse_x - window_padding) / cell_size)
    mouse_y = int((mouse_y - window_padding) / cell_size)
    for x in range(8):
        for y in range(8):
            color = green_dot_color_hover if x == mouse_x and y == mouse_y else green_dot_color

            if board.choices[x][y]:
                x_pos = int(x * cell_size + window_padding + cell_size / 2)
                y_pos = int(y * cell_size + window_padding + cell_size / 2)
                gfxdraw.aacircle(screen, x_pos, y_pos, green_dot_radius, color)
                gfxdraw.filled_circle(screen, x_pos, y_pos, green_dot_radius, color)


hover_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
hover_surface.fill((120, 120, 120, 100))


def render_hover(screen: pygame.display):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x > window_padding and mouse_y > window_padding:
        mouse_x = int((mouse_x - window_padding) / cell_size)
        mouse_y = int((mouse_y - window_padding) / cell_size)
        if mouse_x < 8 and mouse_y < 8:
            piece = get_piece(mouse_x, mouse_y)
            if piece and not piece.black:
                if mouse_x < 8 and mouse_y < 8:
                    screen.blit(hover_surface, (
                        mouse_x * cell_size + window_padding,
                        mouse_y * cell_size + window_padding
                    ))
