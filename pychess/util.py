from .variables import board


def is_occupied(x: int, y: int):
    return get_piece(x, y) is not None


def get_piece(x: int, y: int):
    for piece in board.pieces:
        if piece.x == x and piece.y == y:
            return piece
    return None
