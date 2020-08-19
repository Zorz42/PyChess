from typing import Optional

from numpy import argwhere, inf, ndarray

from .pieces import Piece
from .util import move, undo, get_board_state
from .variables import board


def evaluate() -> float:
    result: float = 0
    piece: Piece

    for piece in board.pieces:
        result += piece.weight

    return result


def get_all_moves(ignore_king: bool = True) -> list:
    result: list = []
    piece: Piece

    for piece in reversed(board.pieces):
        if piece.black:
            piece.update_board(ignore_king)
            moves = piece.scan_board()

            x: int
            y: int
            for x, y in argwhere(moves):
                result.append(((piece.x, piece.y), (x, y)))

    return result


def play() -> Optional[tuple]:
    new_game_moves = get_all_moves(ignore_king=False)

    best_move: int = -inf
    best_move_found: Optional[tuple] = None
    new_game_move: Optional[tuple]

    for new_game_move in new_game_moves:
        move(*new_game_move)
        value = minimax(3, -inf, inf, True)
        undo()
        if value >= best_move:
            best_move = value
            best_move_found = new_game_move

    print(best_move, end='\t - \t')

    if best_move_found:
        move(*best_move_found)
        return best_move_found

def minimax(depth: int, alpha: int, beta: int, maximising: bool) -> int:
    if not depth:
        return -evaluate()

    new_game_moves = get_all_moves()

    best_score: int = -inf if maximising else inf
    move_: tuple

    for move_ in new_game_moves:
        move(*move_)

        state = get_board_state()

        if state in board.transposition:
            current_score: int = board.transposition[state]
        else:
            current_score: int = minimax(depth - 1, alpha, beta, not maximising)

        best_score = max(best_score, current_score) if maximising else min(best_score, current_score)
        undo()

        if maximising:
            alpha = max(alpha, best_score)
        else:
            beta = min(beta, best_score)
        if beta <= alpha:
            return best_score

        board.transposition[state] = current_score

    return best_score
