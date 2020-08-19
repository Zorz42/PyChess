from numpy import full, ndarray


class Board:
    class State:
        none = 0
        won = 1
        lost = 2
        draw = 3

    state: int = State.none

    choices: ndarray = full((8, 8), False)
    pieces: list = []
    pending = None

    white_king = None
    black_king = None

    moves_stack = []
    eaten_stack = []

    transposition = {}


board = Board()

cell_size = 64
window_padding = 40

use_tts_for_player = True
use_tts_for_computer = True

if use_tts_for_player or use_tts_for_computer:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
