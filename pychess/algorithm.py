from numpy import argwhere, inf

from .util import move, undo
from .variables import board


def evaluate():
    result = 0
    for piece in board.pieces:
        result += piece.weight
    return result


def get_all_moves():
    result = []
    for piece in reversed(board.pieces):
        if piece.black:
            piece.update_board(ignore_king=True)
            moves = piece.scan_board()
            for x, y in argwhere(moves):
                result.append(((piece.x, piece.y), (x, y)))
    return result


def play():
    new_game_moves = get_all_moves()
    best_move = -inf
    best_move_found = None
    for new_game_move in new_game_moves:
        move(*new_game_move)
        value = minimax(2, -inf, inf, True)
        undo()
        if value >= best_move:
            best_move = value
            best_move_found = new_game_move

    if best_move_found:
        move(*best_move_found)


def minimax(depth, alpha, beta, maximising):
    if not depth:
        return -evaluate()

    new_game_moves = get_all_moves()

    best_move = -inf if maximising else inf

    for move_ in new_game_moves:
        move(*move_)
        best_move = max(best_move, minimax(depth - 1, alpha, beta, False)) if maximising else \
            min(best_move, minimax(depth - 1, alpha, beta, True))
        undo()
        if maximising:
            alpha = max(alpha, best_move)
        else:
            beta = min(beta, best_move)
        if beta <= alpha:
            return best_move
    return best_move
