from typing import Optional
from hashlib import sha1
from numpy import full

from .variables import board


def get_piece(x: int, y: int) -> Optional['Piece']:
    return board.cached_board[x][y]


def move(old: tuple, new: tuple, store_move: bool = True) -> Optional['Piece']:
    piece_to_be_eaten = get_piece(new[0], new[1])
    if piece_to_be_eaten and piece_to_be_eaten in board.pieces:
        board.pieces.remove(piece_to_be_eaten)
    board.cached_board[new[0]][new[1]] = None

    if store_move:
        board.moves_stack.append((old, new))
        board.eaten_stack.append(piece_to_be_eaten)

    piece = get_piece(old[0], old[1])
    if piece:
        piece.x = new[0]
        piece.y = new[1]
        board.cached_board[old[0]][old[1]] = None
        board.cached_board[new[0]][new[1]] = piece

    return piece


def undo() -> None:
    if len(board.moves_stack) == 0:
        return

    last_move = board.moves_stack.pop()
    last_eaten = board.eaten_stack.pop()

    move(last_move[1], last_move[0], store_move=False)
    if last_eaten:
        board.pieces.append(last_eaten)
        board.cached_board[last_eaten.x][last_eaten.y] = last_eaten


def get_board_state() -> str:
    state = full((8, 8), -1)
    for piece in board.pieces:
        state[piece.x][piece.y] = piece.texture_y + piece.black * 10
    return sha1(state).hexdigest()


def are_pieces_stale(black: bool) -> bool:
    for piece in board.pieces:
        if black == piece.black and piece.can_move():
            return False
    return True


def get_game_state() -> board.State:
    board_state = get_board_state()

    if board_state in board.state_cache:
        return board.state_cache[board_state]

    if are_pieces_stale(black=False):
        game_state = board.State.lost if board.white_king.in_danger() else board.State.draw
    elif are_pieces_stale(black=True):
        game_state = board.State.won if board.black_king.in_danger() else board.State.draw
    else:
        game_state = board.State.playing

    board.state_cache[board_state] = game_state
    return game_state


def convert_to_algebraic_notation(x, y) -> str:
    return 'abcdefgh'[x] + str(8 - y)
