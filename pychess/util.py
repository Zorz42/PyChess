from .variables import board


def get_piece(x: int, y: int):
    for piece in board.pieces:
        if piece.x == x and piece.y == y:
            return piece
    return None


def is_check(king):
    # TODO: This!
    return False


def is_stale(piece):
    return not piece.can_move()


def is_checkmate(king):
    return is_check(king) and is_stale(king)


def is_stalemate(black):
    king = board.black_king if black else board.white_king

    check = is_check(king)
    stale = True

    for piece in board.pieces:
        if (black and piece.black) or (not black and not piece.black):
            continue
        stale &= is_stale(piece)

    return not check and stale
