import os

import pygame
from numpy import full

from .pieces import Rook, Knight, Bishop, Queen, King, Pawn
from .renderers import render_board, render_pieces, render_choices
from .util import is_occupied, get_piece
from .variables import cell_size, window_padding, board


def init():
    icon = pygame.image.load(os.path.dirname(__file__) + '/resources/icon.png')

    pygame.init()
    pygame.display.set_caption('PyChess')
    pygame.display.set_icon(icon)

    window_size = cell_size * 8 + window_padding * 2
    screen = pygame.display.set_mode((window_size, window_size))

    for is_black in (True, False):
        for pawn_x in range(8):
            board.pieces.append(Pawn(pawn_x, 1 if is_black else 6, is_black))

        other_y = 0 if is_black else 7
        for i, piece in enumerate((Rook, Knight, Bishop)):
            board.pieces.append(piece(i, other_y, is_black))
            board.pieces.append(piece(7 - i, other_y, is_black))
        board.pieces.append(Queen(3, other_y, is_black))
        board.pieces.append(King(4, other_y, is_black))

    return screen


def handle(event: pygame.event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = int((mouse_x - window_padding) / cell_size)
        mouse_y = int((mouse_y - window_padding) / cell_size)

        piece = get_piece(mouse_x, mouse_y)
        if piece is not None and not piece.black:
            board.pending = piece
            board.choices = piece.scan_board()
            return

        if not board.choices[mouse_x][mouse_y]:
            return

        if piece:
            board.pieces.remove(piece)

        board.pending.x = mouse_x
        board.pending.y = mouse_y

        board.pending = None
        board.choices = full((8, 8), False)

        # TODO: Check winner
        # TODO: Run AI


def render(screen: pygame.display):
    render_board(screen, cell_size, window_padding)
    render_pieces(screen)
    render_choices(screen)

    pygame.display.flip()
