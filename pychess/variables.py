from numpy import full


class Board:
    active = True

    choices = full((8, 8), False)
    pieces = []
    pending = None

    white_king = None
    black_king = None

    moves_stack = []
    eaten_stack = []


board = Board()

cell_size = 64
window_padding = 40
