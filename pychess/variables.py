from numpy import full


class Board:
    choices = full((0, 0), False)
    pieces = []


board = Board()

cell_size = 64
window_padding = 40
