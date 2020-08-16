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
        pass

    def render(self):
        pass

# scan_board(): return full((8, 8), False)
