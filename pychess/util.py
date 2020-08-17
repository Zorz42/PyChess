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


def is_check(king):
    # Get all positions where king would be in danger (king.get_danger())
    # If danger[king_x][king_y] is true, king is in check
    return False


def is_stalemate(king):
    # Get all positions where king can move
    # If everything is false, it is stalemate
    # Pro tip: Numpy probably has something to quickly check if whole 2d array is false
    return False


def is_checkmate(king):
    return is_check(king) and is_stalemate(king)
