import pygame
from pygame import gfxdraw

from .util import get_piece
from .variables import cell_size, window_padding, board, window_size

green_dot_radius = 11
green_dot_color = (11, 218, 81)
green_dot_color_hover = (8, 163, 61)
shadow_radius = 8


def render_background(screen: pygame.display) -> None:
    for i in range(window_padding):
        pygame.draw.rect(screen, (int(i / 1.75), int(i / 1.75), int(i / 1.75)),
                         (i, i, window_size - i * 2, window_size - i * 2))


def render_board(screen: pygame.display) -> None:
    render_background(screen)

    pygame.draw.rect(screen, (150, 150, 150),
                     (window_padding - 1,
                      window_padding - 1,
                      window_size - window_padding * 2 + 2,
                      window_size - window_padding * 2 + 2
                      ))
    for x in range(8):
        for y in range(8):
            color = (200, 200, 200) if (x + y) % 2 else (130, 130, 130)
            pygame.draw.rect(screen, color, (
                y * cell_size + window_padding,
                x * cell_size + window_padding,
                cell_size,
                cell_size,
            ))


def render_pieces(screen: pygame.display) -> None:
    for piece in board.pieces:
        piece.render(screen)


def render_choices(screen: pygame.display) -> None:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x = int((mouse_x - window_padding) / cell_size)
    mouse_y = int((mouse_y - window_padding) / cell_size)
    for x in range(8):
        for y in range(8):
            color = green_dot_color_hover if x == mouse_x and y == mouse_y else green_dot_color

            if board.choices[x][y]:
                if get_piece(x, y):
                    x_pos = int(x * cell_size + window_padding)
                    y_pos = int(y * cell_size + window_padding)
                    gfxdraw.box(screen,
                                (x_pos, y_pos, cell_size, cell_size),
                                (230, 20, 12, 130))
                else:
                    x_pos = int(x * cell_size + window_padding + cell_size / 2)
                    y_pos = int(y * cell_size + window_padding + cell_size / 2)
                    for i in range(1, shadow_radius + 1):
                        if (x + y) % 2:
                            multiplicator = int(30 - 30 / shadow_radius * i) + 170
                        else:
                            multiplicator = int(20 - 20 / shadow_radius * i) + 110
                        shadow_color = (multiplicator, multiplicator, multiplicator)
                        pygame.draw.circle(screen, shadow_color, (x_pos, y_pos), green_dot_radius + shadow_radius - i)
                    gfxdraw.aacircle(screen, x_pos, y_pos, green_dot_radius, color)
                    gfxdraw.filled_circle(screen, x_pos, y_pos, green_dot_radius, color)


def render_hover(screen: pygame.display) -> None:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x > window_padding and mouse_y > window_padding:
        mouse_x = int((mouse_x - window_padding) / cell_size)
        mouse_y = int((mouse_y - window_padding) / cell_size)
        if mouse_x < 8 and mouse_y < 8:
            piece = get_piece(mouse_x, mouse_y)
            if piece and not piece.black:
                if mouse_x < 8 and mouse_y < 8:
                    gfxdraw.box(screen, (
                        mouse_x * cell_size + window_padding,
                        mouse_y * cell_size + window_padding,
                        cell_size,
                        cell_size
                    ), (120, 120, 120, 100))
