import pygame
from .pieces import pieces


def is_occupied(x: int, y: int):
    return get_piece(x, y) is not None


def get_piece(x: int, y: int):
    for piece in pieces:
        if piece.x == x and piece.y == y:
            return piece
    return None


def render_board(screen: pygame.display, cell_size: int, window_padding: int):
    screen.fill((10, 10, 10))

    for x in range(8):
        for y in range(8):
            color = (200, 200, 200) if (x + y) % 2 else (130, 130, 130)
            pygame.draw.rect(
                screen,
                color,
                (
                    y * cell_size + window_padding,
                    x * cell_size + window_padding,
                    cell_size,
                    cell_size,
                )
            )


def render_pieces(screen: pygame.display):
    for piece in pieces:
        piece.render(screen)
