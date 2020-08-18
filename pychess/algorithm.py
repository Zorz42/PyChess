from numpy import argwhere, inf

from .util import move, undo
from .variables import board


def evaluate():
    result = 0
    for piece in board.pieces:
        result += piece.weight
    return result


def play():
    best_score = -inf
    best_move = None

    for piece in board.pieces:
        if piece.black:
            moves = piece.scan_board()
            for x, y in argwhere(moves):
                current_move = (piece.x, piece.y), (x, y)
                move(*current_move)

                current_score = minimax(1, -inf, inf, True)
                undo()

                if current_score > best_score:
                    best_move = current_move
                    best_score = current_score

    if best_move:
        move(*best_move, store_move=False)


def minimax(depth, alpha, beta, maximising=True):
    if not depth:
        return -evaluate()

    best_score = -inf if maximising else inf
    for piece in board.pieces:
        if piece.black == maximising:
            moves = piece.scan_board()
            for x, y in argwhere(moves):
                move((piece.x, piece.y), (x, y))
                if maximising:
                    best_score = max(minimax(depth - 1, 0, 0, False), best_score)
                else:
                    best_score = min(minimax(depth - 1, 0, 0, True), best_score)
                undo()
    return best_score
