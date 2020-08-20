from abc import abstractmethod
from os import path
from typing import List

import pygame
from numpy import full, argwhere, ndindex, ndarray

from .util import get_piece, move, undo
from .variables import cell_size, window_padding, board


class Piece:
    texture: pygame.image = pygame.image.load(path.dirname(__file__) + '/resources/pieces.png')

    texture_y: int = None

    _weight: int = None
    _weights: List[List[int]] = None

    _black_weights: List[List[int]] = None
    _white_weights: List[List[int]] = None

    def __init__(self, x: int, y: int, black: bool):
        self.x = x
        self.y = y
        self.black = black
        self._saved_board = full((8, 8), False)

    def can_move(self) -> bool:
        self.update_board()
        return not (~self.scan_board()).all()

    def protect_king(self):
        king = board.black_king if self.black else board.white_king

        x: int
        y: int
        for x, y in argwhere(self._saved_board):
            move((self.x, self.y), (x, y))
            if king.in_danger():
                self._saved_board[x][y] = False
            undo()

    def scan_board(self) -> ndarray:
        return self._saved_board

    @abstractmethod
    def update_board(self, ignore_king: bool = False):
        pass

    @property
    def weight(self) -> float:
        if not self._black_weights and self.black:
            self._black_weights = self._weights[::-1]
        if not self._white_weights and not self.black:
            self._white_weights = self._weights

        base_weight = -self._weight if self.black else self._weight
        position_weight = self._black_weights[self.y][self.x] if self.black else self._white_weights[self.y][self.x]
        return base_weight + position_weight

    def render(self, screen: pygame.display):
        screen.blit(self.texture, (
            (self.x * cell_size) + window_padding,
            (self.y * cell_size) + window_padding
        ), (
                        self.texture_y * cell_size,
                        self.black * cell_size,
                        cell_size,
                        cell_size
                    )
                    )


class King(Piece):
    texture_y = 0

    _weight = 900
    _weights = [
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0],
    ]

    def __init__(self, x: int, y: int, black: bool):
        super().__init__(x, y, black)

        if self.black:
            board.black_king = self
        else:
            board.white_king = self

    def in_danger(self) -> bool:
        for other in board.pieces:
            if self.black != other.black:
                if isinstance(other, Pawn):
                    danger = other.get_attacks()
                else:
                    other.update_board(ignore_king=True)
                    danger = other.scan_board()
                if danger[self.x][self.y]:
                    return True
        return False

    def update_board(self, ignore_king: bool = False):
        self._saved_board = full((8, 8), False)

        x: int
        y: int
        for x, y in ndindex((3, 3)):
            abs_x = self.x + x - 1
            abs_y = self.y + y - 1
            if 0 <= abs_x < 8 and 0 <= abs_y < 8:
                curr_piece = get_piece(abs_x, abs_y)
                self._saved_board[abs_x][abs_y] = not curr_piece or self.black != curr_piece.black

        self._saved_board[self.x][self.y] = False

        if not ignore_king:
            self.protect_king()


class Queen(Piece):
    texture_y = 1

    _weight = 90
    _weights = [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    ]

    def update_board(self, ignore_king: bool = False):
        self._saved_board = full((8, 8), False)

        for orientation in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
            x, y = self.x, self.y
            for pos in range(1, 8):
                x += orientation[0]
                y += orientation[1]

                if x < 0 or x > 7 or y < 0 or y > 7:
                    break

                curr_piece = get_piece(x, y)
                if curr_piece:
                    if self.black != curr_piece.black:
                        self._saved_board[x][y] = True
                    break

                self._saved_board[x][y] = True

        if not ignore_king:
            self.protect_king()


class Rook(Piece):
    texture_y = 4

    _weight = 50
    _weights = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
    ]

    def update_board(self, ignore_king: bool = False):
        self._saved_board = full((8, 8), False)

        for orientation in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            for pos in range(1, 8):
                x: int = self.x + pos * orientation[0]
                y: int = self.y + pos * orientation[1]

                if x < 0 or x > 7 or y < 0 or y > 7:
                    break

                curr_piece = get_piece(x, y)
                if curr_piece:
                    if self.black != curr_piece.black:
                        self._saved_board[x][y] = True
                    break

                self._saved_board[x][y] = True

        if not ignore_king:
            self.protect_king()


class Bishop(Piece):
    texture_y = 2

    _weight = 30
    _weights = [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    ]

    def update_board(self, ignore_king: bool = False):
        self._saved_board = full((8, 8), False)

        for orientation in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            for pos in range(1, 8):
                x: int = self.x + pos * orientation[0]
                y: int = self.y + pos * orientation[1]

                if x < 0 or x > 7 or y < 0 or y > 7:
                    break

                curr_piece = get_piece(x, y)
                if curr_piece:
                    if self.black != curr_piece.black:
                        self._saved_board[x][y] = True
                    break

                self._saved_board[x][y] = True

        if not ignore_king:
            self.protect_king()


class Knight(Piece):
    texture_y = 3

    _weight = 30
    _weights = [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
        [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    ]

    def update_board(self, ignore_king: bool = False):
        self._saved_board = full((8, 8), False)

        target: tuple
        for target in ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (2, -1), (1, -2)):
            x = self.x + target[0]
            y = self.y + target[1]

            if x < 0 or x > 7 or y < 0 or y > 7:
                continue

            curr_piece = get_piece(x, y)
            self._saved_board[x][y] = not curr_piece or self.black != curr_piece.black

        if not ignore_king:
            self.protect_king()


class Pawn(Piece):
    texture_y = 5

    _weight = 10
    _weights = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ]

    def update_board(self, ignore_king: bool = False):
        self._saved_board = full((8, 8), False)
        if not 0 < self.y < 7:
            return

        direction = 1 if self.black else -1

        y: int
        for y in range(2 if (self.y == (1 if self.black else 6)) else 1):
            abs_y = self.y + y * direction + direction
            if 0 <= abs_y < 8:
                if get_piece(self.x, abs_y):
                    break
                self._saved_board[self.x][abs_y] = True

        x: int
        for x in (-1, 1):
            piece = get_piece(self.x + x, self.y + direction)
            if piece and self.black != piece.black:
                self._saved_board[self.x + x][self.y + direction] = True

        if not ignore_king:
            self.protect_king()

    def get_attacks(self) -> ndarray:
        choices = (full((8, 8), False))

        direction = 1 if self.black else -1
        if 0 <= self.y + direction < 8:
            if self.x < 7:
                choices[self.x + 1][self.y + direction] = True
            if self.x > 0:
                choices[self.x - 1][self.y + direction] = True

        return choices
