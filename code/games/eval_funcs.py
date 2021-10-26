from Games import *

def eval_checkers_1(game: CheckersGame) -> int:
    dim = game.getDim()

    if len(game.getValidMoves()) == 0:
        # game is finished, so just count pieces
        w_count = 0
        b_count = 0
        for row in range(dim):
            for col in range(dim):
                piece = game.getPieceAtPos(row, col)
                if piece == '.':
                    continue
                elif piece == 'w':
                    w_count += 1
                elif piece == 'W':
                    w_count += 2
                elif piece == 'b':
                    b_count += 1
                elif piece == 'B':
                    b_count += 2
                else:
                    raise ValueError("Unknown checkers piece ({}) at pos ({},{})".format(piece, row, col))

        if w_count == b_count:
            return 0
        elif w_count > b_count:
            return -1 * 2**32
        else:
            return 2**32

    val = 0

    for row in range(dim):
        for col in range(dim):
            piece = game.getPieceAtPos(row, col)
            if piece == '.':
                continue
            elif piece.lower() == 'w':
                # Base piece value
                val -= 100

                # Bonus for pieces in the home row (controlling king spots)
                if row == 0:
                    val -= 100
                
                # Bonus for kings
                if piece == 'W':
                    val -= 200
            elif piece.lower() == 'b':
                val += 100

                if row == dim-1:
                    val += 100
                
                if piece == 'B':
                    val += 200

    if game.getWhoseMove() == 'WHITE':
        val -= 20
    else:
        val += 20

    return val

def _eval_othello_1_position_multiplier(row: int, col: int, dim: int) -> int:
    # corners
    if (row == 0 or row == (dim - 1)) and (col == 0 or col == (dim - 1)):
        return 16
    
    # edges
    if row == 0 or row == (dim - 1) or col == 0 or col == (dim - 1):
        return 8

    # one away from edges
    if row == 1 or row == (dim - 2) or col == 1 or col == (dim - 2):
        return 0
    
    # middle
    assert row > 1 and row < (dim - 2) and col > 1 and col < (dim - 2)
    return 1

def eval_othello_1(game: OthelloGame) -> int:
    dim = game.getDim()

    if len(game.getValidMoves()) == 0:
        white_count = 0
        black_count = 0
        for row in range(dim):
            for col in range(dim):
                piece = game.getPieceAtPos(row, col)
                if piece == 'W':
                    white_count += 1
                elif piece == 'B':
                    black_count += 1
        if white_count == black_count:
            return 0
        elif white_count > black_count:
            return -1 * 2**32
        else:
            return 2**32
    
    val = 0

    for row in range(dim):
        for col in range(dim):
            piece = game.getPieceAtPos(row, col)
            if piece == '.':
                continue
            sign = 1 if piece == 'B' else -1
            val += sign * _eval_othello_1_position_multiplier(row, col, dim)

    return val
            