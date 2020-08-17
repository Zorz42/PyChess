from .variables import board


def get_piece(x: int, y: int):
    for piece in board.pieces:
        if piece.x == x and piece.y == y:
            return piece
    return None


def get_board_weight():
    result = 0
    for piece in board.pieces:
        result += piece.weight
    return result
