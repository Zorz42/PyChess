from .variables import board


def get_piece(x: int, y: int):
    for piece in board.pieces:
        if piece.x == x and piece.y == y:
            return piece
    return None


def move(old: tuple, new: tuple, store_move=True):
    piece_to_be_eaten = get_piece(new[0], new[1])
    if piece_to_be_eaten:
        board.pieces.remove(piece_to_be_eaten)

    if store_move:
        board.moves_stack.append((old, new))
        board.eaten_stack.append(piece_to_be_eaten)

    piece = get_piece(old[0], old[1])
    if piece:
        piece.x = new[0]
        piece.y = new[1]
    return piece


def undo():
    if len(board.moves_stack) == 0:
        return

    last_move = board.moves_stack.pop()
    last_eaten = board.eaten_stack.pop()

    move(last_move[1], last_move[0], store_move=False)
    if last_eaten:
        board.pieces.append(last_eaten)


def is_check(king):
    return king.in_danger()


def is_stale(piece):
    return not piece.can_move()


def is_checkmate(king):
    is_stalemate_ = True
    for piece in board.pieces:
        if king.black != piece.black:
            if not is_stale(piece):
                is_stalemate_ = False
    return is_check(king) and is_stalemate_


def is_stalemate(black):
    for piece in board.pieces:
        if black != piece.black:
            if not is_stale(piece):
                return False

    return not is_check(board.black_king if black else board.white_king)


def update_pieces():
    for piece in board.pieces:
        piece.update_board()
