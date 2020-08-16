from pychess import board


def is_occupied(x: int, y: int):
    for piece in board:
        if piece.x == x and piece.y == y:
            return True
    return False
