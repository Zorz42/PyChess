from abc import abstractmethod
from os import path

import pygame
from numpy import full

from .util import get_piece
from .variables import cell_size, window_padding, board


class Piece:
    texture = pygame.image.load(path.dirname(__file__) + '/resources/pieces.png')

    texture_y = None
    _weight = None

    def __init__(self, x: int, y: int, black: bool):
        self.x = x
        self.y = y
        self.black = black

    def can_move(self):
        return not (~self.scan_board()).all()

    @abstractmethod
    def scan_board(self):
        pass

    @property
    def weight(self):
        return -self._weight if self.black else self._weight

    def render(self, screen):
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
    _weight = 90

    def __init__(self, x: int, y: int, black: bool):
        super().__init__(x, y, black)

        if self.black:
            board.black_king = self
        else:
            board.white_king = self

    def in_danger(self):
        for other in board.pieces:
            if other != self and self.black != other.black:
                if isinstance(other, Pawn):
                    danger = other.get_attacks()
                elif isinstance(other, King):
                    danger = other.scan_board(ignore_king=True)
                else:
                    danger = other.scan_board()
                if danger[self.x][self.y]:
                    return True
        return False

    def scan_board(self, ignore_king=False):
        choices = full((8, 8), False)
        for x in range(3):
            for y in range(3):
                abs_x = self.x + x - 1
                abs_y = self.y + y - 1
                if 0 <= abs_x < 8 and 0 <= abs_y < 8:
                    curr_piece = get_piece(abs_x, abs_y)
                    choices[abs_x][abs_y] = not curr_piece or self.black != curr_piece.black

        choices[self.x][self.y] = False
        prev_x, prev_y = self.x, self.y
        if not ignore_king:
            for x in range(8):
                for y in range(8):
                    if choices[x][y]:
                        self.x, self.y = x, y
                        piece = get_piece(x, y)
                        if piece:
                            board.pieces.remove(piece)
                        if self.in_danger():
                            choices[x][y] = False
                        if piece:
                            board.pieces.append(piece)
        self.x, self.y = prev_x, prev_y

        return choices


class Queen(Piece):
    texture_y = 1
    _weight = 9

    def scan_board(self):
        choices = full((8, 8), False)

        for o in (True, False):
            for start, end, step in ((-1, -1, -1), (1, 8, 1)):
                for pos in range((self.y if o else self.x) + start, end, step):
                    x = self.x if o else pos
                    y = pos if o else self.y

                    curr_piece = get_piece(x, y)
                    if curr_piece:
                        if not self.black and curr_piece.black:
                            choices[x][y] = True
                        elif self.black and not curr_piece.black:
                            choices[x][y] = True
                        break

                    choices[x][y] = True

        for orientation in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            for pos in range(1, 8):
                x = self.x + pos * orientation[0]
                y = self.y + pos * orientation[1]

                if x < 0 or x > 7 or y < 0 or y > 7:
                    continue

                curr_piece = get_piece(x, y)
                if curr_piece is not None:
                    if not self.black and curr_piece.black:
                        choices[x][y] = True
                    elif self.black and not curr_piece.black:
                        choices[x][y] = True
                    break

                choices[x][y] = True

        return choices


class Rook(Piece):
    texture_y = 4
    _weight = 5

    def scan_board(self):
        choices = full((8, 8), False)

        for o in (True, False):
            for start, end, step in ((-1, -1, -1), (1, 8, 1)):
                for pos in range((self.y if o else self.x) + start, end, step):
                    x = self.x if o else pos
                    y = pos if o else self.y

                    curr_piece = get_piece(x, y)
                    if curr_piece:
                        if not self.black and curr_piece.black:
                            choices[x][y] = True
                        elif self.black and not curr_piece.black:
                            choices[x][y] = True
                        break

                    choices[x][y] = True

        return choices


class Bishop(Piece):
    texture_y = 2
    _weight = 3

    def scan_board(self):
        choices = full((8, 8), False)

        for orientation in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            for pos in range(1, 8):
                x = self.x + pos * orientation[0]
                y = self.y + pos * orientation[1]

                if x < 0 or x > 7 or y < 0 or y > 7:
                    continue

                curr_piece = get_piece(x, y)
                if curr_piece is not None:
                    if not self.black and curr_piece.black:
                        choices[x][y] = True
                    elif self.black and not curr_piece.black:
                        choices[x][y] = True
                    break

                choices[x][y] = True

        return choices


class Knight(Piece):
    texture_y = 3
    _weight = 3

    def scan_board(self):
        choices = full((8, 8), False)

        for target in ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (2, -1), (1, -2)):
            x = self.x + target[0]
            y = self.y + target[1]

            if x < 0 or x > 7 or y < 0 or y > 7:
                continue

            curr_piece = get_piece(x, y)

            if self.black:
                choices[x][y] = not curr_piece or not curr_piece.black
            else:
                choices[x][y] = not curr_piece or curr_piece.black

        return choices


class Pawn(Piece):
    texture_y = 5
    _weight = 1

    def scan_board(self):
        choices = full((8, 8), False)
        if not 0 < self.y < 7:
            return choices

        direction = 1 if self.black else -1

        for y in range(2 if (self.y == (1 if self.black else 6)) else 1):
            abs_y = self.y + y * direction + direction
            if 0 <= abs_y < 8:
                if get_piece(self.x, abs_y):
                    break
                choices[self.x][abs_y] = True

        for x in (-1, 1):
            piece = get_piece(self.x + x, self.y + direction)
            if piece and self.black != piece.black:
                choices[self.x + x][self.y + direction] = True

        return choices

    def get_attacks(self):
        choices = full((8, 8), False)

        if not self.x < 1 and not self.x > 6:
            direction = 1 if self.black else -1
            choices[self.x + 1][self.y + direction] = True
            choices[self.x - 1][self.y + direction] = True

        return choices
