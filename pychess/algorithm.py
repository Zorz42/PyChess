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
                # print(piece, f'from {piece.x} {piece.y} can move to {x} {y}')

                current_move = (piece.x, piece.y), (x, y)
                move(*current_move)

                current_score = minimax(3, -inf, inf, True)
                undo()

                if current_score > best_score:
                    best_move = current_move
                    best_score = current_score

    if best_move:
        move(*best_move, store_move=False)


def minimax(depth, alpha, beta, maximising=True):
    # Very good AI
    from random import randint
    return randint(-100, 100)
