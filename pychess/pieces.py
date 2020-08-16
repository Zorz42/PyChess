from numpy import full
from abc import abstractmethod
from .variables import cell_size, window_padding

import os
import pygame

pieces = []


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
        bool_board = full((8, 8), False)
        for x in range(3):
            for y in range(3):
                abs_x = self.x + x - 1
                abs_y = self.y + y - 1
                if 0 <= abs_x <= 8 and 0 <= abs_y <= 8:
                    bool_board[abs_x][abs_y] = True
                bool_board[self.x][self.y] = False
        return bool_board


class Queen(Piece):
    texture_y = 0

    def scan_board(self):
        pass


class Rooks(Piece):
    texture_y = 0

    def scan_board(self):
        pass
