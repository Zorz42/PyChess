from numpy import full


class Board:
    choices = full((8, 8), False)
    pieces = []
    pending = None


board = Board()

cell_size = 64
window_padding = 40
