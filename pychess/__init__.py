import pygame
from numpy import full

from .pieces import Rook, Knight, Bishop, Queen, King, Pawn
from .renderers import render_board, render_pieces, render_choices
from .util import is_occupied, get_piece
from .variables import cell_size, window_padding, board


def init():
    pygame.init()
    pygame.display.set_caption('PyChess')

    window_size = cell_size * 8 + window_padding * 2
    screen = pygame.display.set_mode((window_size, window_size))

    for color in ('black', 'white'):
        is_black = True if color == 'black' else False
        for pawn_x in range(8):
            pawn_y = 1 if color == 'black' else 6
            # board.pieces.append((Pawn(pawn_x, pawn_y, is_black)))

        other_y = 0 if color == 'black' else 7
        board.pieces.append(Rook(0, other_y, is_black))
        board.pieces.append(Knight(1, other_y, is_black))
        board.pieces.append(Bishop(2, other_y, is_black))
        board.pieces.append(Queen(3, other_y, is_black))
        board.pieces.append(King(4, other_y, is_black))
        board.pieces.append(Bishop(5, other_y, is_black))
        board.pieces.append(Knight(6, other_y, is_black))
        board.pieces.append(Rook(7, other_y, is_black))

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
