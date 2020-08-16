from numpy import full
from abc import abstractmethod

board = []


class Piece:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @abstractmethod
    def scan_board(self):
        pass

    @abstractmethod
    def render(self):
        pass


class King(Piece):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def scan_board(self):
        bool_board = full((8, 8), False)
        for x in range(3):
            for y in range(3):
                abs_x = self.x + x
                abs_y = self.y + y
                if 0 <= abs_x <= 8 and 0 <= abs_y <= 8:
                    bool_board[abs_x][abs_y] = True
        return bool_board

    def render(self):
        pass
