from numpy import full, ndarray, empty


class Board:
    class State:
        initializing = -1
        playing = 0
        won = 1
        lost = 2
        draw = 3

    state: int = State.initializing

    choices: ndarray = full((8, 8), False)
    pieces: list = []
    pending = None

    white_king = None
    black_king = None

    moves_stack = []
    eaten_stack = []

    transposition = {}
    state_cache = {}

    cached_board = empty((8, 8), dtype=object)


board = Board()

cell_size = 64
window_padding = 40

window_size = cell_size * 8 + window_padding * 2

use_tts_for_player = True
use_tts_for_computer = True
