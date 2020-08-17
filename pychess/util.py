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
    return king.get_danger()[king.x][king.y]


def is_stale(king):
    return not king.can_move()


def is_checkmate(king):
    return is_check(king) and is_stale(king)


def is_stalemate(king):
    return not is_check(king) and is_stale(king)
