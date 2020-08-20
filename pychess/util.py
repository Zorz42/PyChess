from typing import Optional

from numpy import full

from .variables import board


def get_piece(x: int, y: int) -> Optional['Piece']:
    for piece in board.pieces:
        if piece.x == x and piece.y == y:
            return piece
    return None


def move(old: tuple, new: tuple, store_move: bool = True):
    piece_to_be_eaten = get_piece(new[0], new[1])
    if piece_to_be_eaten:
        board.pieces.remove(piece_to_be_eaten)

    if store_move:
        board.moves_stack.append((old, new))
        board.eaten_stack.append(piece_to_be_eaten)

    piece = get_piece(old[0], old[1])
    if piece:
        piece.x = new[0]
        piece.y = new[1]

    return piece


def undo():
    if len(board.moves_stack) == 0:
        return

    last_move = board.moves_stack.pop()
    last_eaten = board.eaten_stack.pop()

    move(last_move[1], last_move[0], store_move=False)
    if last_eaten:
        board.pieces.append(last_eaten)


def is_check(king) -> bool:
    return king.in_danger()


def is_stale(piece) -> bool:
    return not piece.can_move()


def is_checkmate(king) -> bool:
    for piece in board.pieces:
        if king.black == piece.black:
            if piece.can_move():
                return False
    return is_check(king)


def is_stalemate(king) -> bool:
    for piece in board.pieces:
        if king.black == piece.black:
            if piece.can_move():
                return False
    return not is_check(king)


def get_board_state() -> tuple:
    state = full((8, 8), -1)
    for piece in board.pieces:
        state[piece.x][piece.y] = piece.texture_y + piece.black * 10
    return tuple(map(tuple, state))


def convert_to_algebraic_notation(x, y):
    return 'abcdefgh'[x] + str(8 - y)
