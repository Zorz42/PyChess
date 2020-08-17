from .pieces import King
from .variables import board


def get_board_weight():
    result = 0
    for piece in board.pieces:
        result += piece.weight
    return result


def is_check(king: King):
    return king.get_danger()[king.x][king.y]


def is_stale(king: King):
    return (~king.scan_board()).all()


def is_checkmate(king: King):
    return is_check(king) and is_stale(king)


def is_stalemate(king: King):
    return not is_check(king) and is_stale(king)
