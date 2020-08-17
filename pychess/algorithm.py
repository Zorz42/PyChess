from .variables import board


def play():
    # Do move:
    # Call minimax/negamax on all possible start moves?
    # Get best move
    # Modify board.pieces and board.choices
    pass


def evaluate():
    result = 0
    for piece in board.pieces:
        result += piece.weight
    return result


def minimax():
    pass
