from numpy import argwhere, inf

from .util import move, undo, get_board_state, update_pieces
from .variables import board


def evaluate():
    result = 0
    for piece in board.pieces:
        result += piece.weight
    return result


def play():
    update_pieces()
    best_score = -inf
    best_move = None

    for piece in board.pieces:
        if piece.black:
            moves = piece.scan_board()
            for x, y in argwhere(moves):
                current_move = (piece.x, piece.y), (x, y)
                move(*current_move)

                current_score = minimax(3, -inf, inf, True)
                undo()

                if current_score > best_score:
                    best_move = current_move
                    best_score = current_score

    print(best_score, end='\t - \t')

    if best_move:
        move(*best_move, store_move=False)


def minimax(depth, alpha, beta, maximising, use_transposition=True):
    if not depth:
        return -evaluate()

    best_score = -inf if maximising else inf
    for piece in board.pieces:
        if piece.black == maximising:
            moves = piece.scan_board()
            for x, y in argwhere(moves):
                move((piece.x, piece.y), (x, y))

                state = get_board_state()
                if state in board.transposition and use_transposition:
                    current_score = board.transposition[state]
                else:
                    current_score = minimax(depth - 1, alpha, beta, not maximising)

                if maximising:
                    best_score = max(current_score, best_score)
                    alpha = max(best_score, alpha)
                else:
                    best_score = min(current_score, best_score)
                    beta = min(best_score, beta)
                undo()

                if beta <= alpha:
                    return best_score

                board.transposition[state] = current_score

    return best_score
