from os import path

import pygame
from numpy import full

from . import speech
from .algorithm import play
from .messages import display_lost, display_won, display_game_draw, messages_init
from .pieces import Rook, Knight, Bishop, Queen, King, Pawn
from .renderers import render_board, render_pieces, render_choices, render_hover
from .util import get_piece, convert_to_algebraic_notation, move, get_game_state
from .variables import cell_size, window_padding, board


def place_pieces() -> None:
    for is_black in (True, False):
        for pawn_x in range(8):
            board.pieces.append(Pawn(pawn_x, 1 if is_black else 6, is_black))

        other_y = 0 if is_black else 7
        for i, piece in enumerate((Rook, Knight, Bishop)):
            board.pieces.append(piece(i, other_y, is_black))
            board.pieces.append(piece(7 - i, other_y, is_black))
        board.pieces.append(Queen(3, other_y, is_black))
        board.pieces.append(King(4, other_y, is_black))


def display_end_messages() -> None:
    for piece in board.pieces:
        piece.update_board()
    board.state = get_game_state()


def init() -> pygame.display:
    icon = pygame.image.load(path.dirname(__file__) + '/resources/icon.png')

    pygame.init()
    messages_init()
    pygame.display.set_caption('PyChess')
    pygame.display.set_icon(icon)

    window_size = cell_size * 8 + window_padding * 2
    screen = pygame.display.set_mode((window_size, window_size))

    place_pieces()

    return screen


def render(screen: pygame.display) -> None:
    render_board(screen)
    render_pieces(screen)
    if board.state == board.State.playing:
        render_choices(screen)
        render_hover(screen)
    elif board.state == board.State.draw:
        display_game_draw(screen)
    elif board.state == board.State.lost:
        display_lost(screen)
    elif board.state == board.State.won:
        display_won(screen)

    pygame.display.flip()


def handle(screen: pygame.display, event: pygame.event) -> None:
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < window_padding or mouse_y < window_padding:
            return

        mouse_x = int((mouse_x - window_padding) / cell_size)
        mouse_y = int((mouse_y - window_padding) / cell_size)

        if mouse_x > 7 or mouse_y > 7:
            return

        piece = get_piece(mouse_x, mouse_y)
        if piece and not piece.black:
            board.pending = piece
            piece.update_board()
            board.choices = piece.scan_board()
            return

        if not board.choices[mouse_x][mouse_y]:
            return

        if piece:
            board.pieces.remove(piece)
            board.cached_board[piece.x][piece.y] = None

        if variables.use_tts_for_player:
            piece_name = board.pending.__class__.__name__
            old_position = convert_to_algebraic_notation(board.pending.x, board.pending.y)
            new_position = convert_to_algebraic_notation(mouse_x, mouse_y)
            speech.say(f'Player moves {piece_name} from {old_position} to {new_position}')

        move((board.pending.x, board.pending.y), (mouse_x, mouse_y), store_move=False)

        board.pending = None
        board.choices = full((8, 8), False)

        display_end_messages()
        if board.state:
            return

        render(screen)

        from time import time
        start = time()
        computer_move = play()
        print(time() - start)

        if variables.use_tts_for_computer:
            piece_name = get_piece(*computer_move[1]).__class__.__name__
            old_position = convert_to_algebraic_notation(*computer_move[0])
            new_position = convert_to_algebraic_notation(*computer_move[1])
            speech.say(f'Computer moves {piece_name} from {old_position} to {new_position}')

        display_end_messages()
