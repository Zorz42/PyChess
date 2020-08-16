from numpy import full
from abc import abstractmethod

import os
import pygame

board = []


class Piece:
    texture = pygame.image.load(os.path.dirname(__file__) + '/resources/pieces.png')

    texture_x = None
    texture_y = None

    cell_size = 64
    window_padding = 40

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
                (self.x * self.cell_size) + self.window_padding,
                (self.y * self.cell_size) + self.window_padding
            ),
            (
                self.texture_y * self.cell_size,
                self.texture_x * self.cell_size,
                self.cell_size,
                self.cell_size
            )
        )


class King(Piece):
    def __init__(self, x: int, y: int, black: bool):
        super().__init__(x, y, black)

        self.texture_x = 1 if black else 0
        self.texture_y = 0

    def scan_board(self):
        bool_board = full((8, 8), False)
        for x in range(3):
            for y in range(3):
                abs_x = self.x + x
                abs_y = self.y + y
                if 0 <= abs_x <= 8 and 0 <= abs_y <= 8:
                    bool_board[abs_x][abs_y] = True
        return bool_board
