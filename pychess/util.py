from .variables import board


def get_piece(x: int, y: int):
    for piece in board.pieces:
        if piece.x == x and piece.y == y:
            return piece
    return None


def move(old: tuple, new: tuple):
    piece = get_piece(old[0], old[1])
    if piece:
        piece.x = new[0]
        piece.y = new[1]
    return piece


def is_check(king):
    return king.in_danger()


def is_stale(piece):
    return not piece.can_move()


def is_checkmate(king):
    return is_check(king) and is_stale(king)


def is_stalemate(black):
    stale = True
    for piece in board.pieces:
        if black != piece.black:
            if not is_stale(piece):
                stale = False
                break

    return not is_check(board.black_king if black else board.white_king) and stale
