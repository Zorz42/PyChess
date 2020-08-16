import os
import pygame
from abc import abstractmethod

from numpy import full

from .variables import cell_size, window_padding
from .util import get_piece

class Piece:
    texture = pygame.image.load(os.path.dirname(__file__) + '/resources/pieces.png')

    texture_y = None

    def __init__(self, x: int, y: int, black: bool):
        self.x = x
        self.y = y
        self.black = black

    @abstractmethod
    def scan_board(self):
        pass

    def render(self, screen):
        screen.blit(
            self.texture,
            (
                (self.x * cell_size) + window_padding,
                (self.y * cell_size) + window_padding
            ),
            (
                self.texture_y * cell_size,
                self.black * cell_size,
                cell_size,
                cell_size
            )
        )


class King(Piece):
    texture_y = 0

    def scan_board(self):
        choices = full((8, 8), False)
        for x in range(3):
            for y in range(3):
                abs_x = self.x + x - 1
                abs_y = self.y + y - 1
                if 0 <= abs_x < 8 and 0 <= abs_y < 8:
                    curr_piece = get_piece(abs_x, abs_y)
                    choices[abs_x][abs_y] = curr_piece is None or curr_piece.black
        choices[self.x][self.y] = False
        return choices


class Queen(Piece):
    texture_y = 1

    def scan_board(self):
        pass


class Rook(Piece):
    texture_y = 4

    def scan_board(self):
        choices = full((8, 8), False)

        for o in (True, False):
            for start, end, step in ((-1, -1, -1), (1, 8, 1)):
                for pos in range((self.y if o else self.x) + start, end, step):
                    x = self.x if o else pos
                    y = pos if o else self.y

                    curr_piece = get_piece(x, y)
                    if curr_piece is not None:
                        if curr_piece.black:
                            choices[x][y] = True
                        break
                    choices[x][y] = True

        return choices


class Bishop(Piece):
    texture_y = 2

    def scan_board(self):
        pass


class Knight(Piece):
    texture_y = 3

    def scan_board(self):
        pass


class Pawn(Piece):
    texture_y = 5

    def scan_board(self):
        pass
