from abc import abstractmethod
from os import path

import pygame
from numpy import full

from .util import get_piece
from .variables import cell_size, window_padding, board


class Piece:
    texture = pygame.image.load(path.dirname(__file__) + '/resources/pieces.png')

    texture_y = None

    def __init__(self, x: int, y: int, black: bool):
        self.x = x
        self.y = y
        self.black = black

    @abstractmethod
    def scan_board(self, ignore_king=False):
        pass

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

    def scan_board(self, ignore_king=False):
        danger = full((8, 8), False)
        for other in board.pieces:
            if ignore_king:
                break

            if other != self and ((self.black and not other.black) or (not self.black and other.black)):
                if isinstance(other, Pawn):
                    danger |= other.get_attacks()
                else:
                    danger |= other.scan_board(ignore_king=True)

        choices = full((8, 8), False)
        for x in range(3):
            for y in range(3):
                abs_x = self.x + x - 1
                abs_y = self.y + y - 1
                if 0 <= abs_x < 8 and 0 <= abs_y < 8:
                    curr_piece = get_piece(abs_x, abs_y)

                    if self.black:
                        choices[abs_x][abs_y] = not curr_piece or not curr_piece.black
                    else:
                        choices[abs_x][abs_y] = not curr_piece or curr_piece.black

                    if danger[abs_x][abs_y]:
                        choices[abs_x][abs_y] = False

        choices[self.x][self.y] = False
        return choices


class Queen(Piece):
    texture_y = 1

    def scan_board(self, ignore_king=False):
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

                        if not (ignore_king and isinstance(curr_piece, King)):
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

                    if not (ignore_king and isinstance(curr_piece, King)):
                        break

                choices[x][y] = True

        return choices


class Rook(Piece):
    texture_y = 4

    def scan_board(self, ignore_king=False):
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

                        if not (ignore_king and isinstance(curr_piece, King)):
                            break

                    choices[x][y] = True

        return choices


class Bishop(Piece):
    texture_y = 2

    def scan_board(self, ignore_king=False):
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

                    if not (ignore_king and isinstance(curr_piece, King)):
                        break

                choices[x][y] = True

        return choices


class Knight(Piece):
    texture_y = 3

    def scan_board(self, ignore_king=False):
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

    def scan_board(self, ignore_king=False):
        choices = full((8, 8), False)
        if not self.y or self.y > 7:
            return choices

        direction = 1 if self.black else -1

        for y in range(2 if self.y == 6 else 1):
            if self.x < 0 or self.x > 7 or self.y - y + direction < 0 or self.y - y + direction > 7:
                continue
            if get_piece(self.x, self.y - y + direction):
                break
            choices[self.x][self.y - y + direction] = True

        for x in (-1, 1):
            if x < 0 or x > 7 or self.y + direction < 0 or self.y + direction > 7:
                continue
            piece = get_piece(self.x + x, self.y + direction)
            if piece and ((not self.black and piece.black) or (self.black and not piece.black)):
                choices[self.x + x][self.y + direction] = True

        return choices

    def get_attacks(self):
        choices = full((8, 8), False)
        direction = 1 if self.black else -1

        if self.x - 1 < 0 or self.x + 1 > 7 or self.y + direction < 0 or self.y + direction > 7:
            return choices

        choices[self.x + 1][self.y + direction] = True
        choices[self.x - 1][self.y + direction] = True

        return choices
