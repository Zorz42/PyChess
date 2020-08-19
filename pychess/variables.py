from numpy import full


class Board:
    class State:
        playing = 0
        won = 1
        lost = 2
        draw = 3

    state = State.playing

    choices = full((8, 8), False)
    pieces = []
    pending = None

    white_king = None
    black_king = None

    moves_stack = []
    eaten_stack = []

    transposition = {}


board = Board()

cell_size = 64
window_padding = 40
