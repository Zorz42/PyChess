from os import path

import pygame
from numpy import full

from .algorithm import play
from .pieces import Rook, Knight, Bishop, Queen, King, Pawn
from .renderers import render_board, render_pieces, render_choices, render_hover
from .util import get_piece, is_checkmate, is_stalemate
from .variables import cell_size, window_padding, board


def place_pieces():
    """
    for is_black in (True, False):
        for pawn_x in range(8):
            board.pieces.append(Pawn(pawn_x, 1 if is_black else 6, is_black))

        other_y = 0 if is_black else 7
        for i, piece in enumerate((Rook, Knight, Bishop)):
            board.pieces.append(piece(i, other_y, is_black))
            board.pieces.append(piece(7 - i, other_y, is_black))
        board.pieces.append(Queen(3, other_y, is_black))
        board.pieces.append(King(4, other_y, is_black))
    """

    # Example that does not work
    # Try to move pawn (it does not work) and other pieces (they work)
    board.pieces.append(Pawn(0, 6, False))
    board.pieces.append(King(5, 5, False))
    board.pieces.append(Rook(7, 4, False))
    board.pieces.append(King(7, 7, True))


def display_end_messages():
    if is_checkmate(board.white_king):
        print('Player lost')
        board.state = board.State.lost
        return

    if is_checkmate(board.black_king):
        print('Player won')
        board.state = board.State.won
        return

    if is_stalemate(black=True) or is_stalemate(black=False):
        print('Game draw')
        board.state = board.State.draw
        return


def init():
    icon = pygame.image.load(path.dirname(__file__) + '/resources/icon.png')

    pygame.init()
    pygame.display.set_caption('PyChess')
    pygame.display.set_icon(icon)

    window_size = cell_size * 8 + window_padding * 2
    screen = pygame.display.set_mode((window_size, window_size))

    place_pieces()

    return screen


def render(screen: pygame.display):
    render_board(screen)
    render_pieces(screen)
    render_choices(screen)
    render_hover(screen)

    pygame.display.flip()


def handle(screen: pygame.display, event: pygame.event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < window_padding or mouse_y < window_padding:
            return

        mouse_x = int((mouse_x - window_padding) / cell_size)
        mouse_y = int((mouse_y - window_padding) / cell_size)

        if mouse_x > 7 or mouse_y > 7:
            return

        piece = get_piece(mouse_x, mouse_y)
        if piece: # and not piece.black:
            board.pending = piece
            piece.update_board()
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

        display_end_messages()
        if board.state:
            return

        render(screen)

        from time import time
        start = time()
        play()
        print(time() - start)

        display_end_messages()
