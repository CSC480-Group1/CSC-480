from Games import *
import numpy as np
from functools import reduce
from Connect4 import BLACK, WHITE, NONE, diagonalsNeg, diagonalsPos
from itertools import groupby, chain
import random

class GameEvalFuncs:
    def __init__(self, evaluator, remove_depth_from_score=(lambda s, d: s), depth_affected_score=(lambda s, d: s)):
        self.evaluator = evaluator
        self.remove_depth_from_score = remove_depth_from_score
        self.depth_affected_score = depth_affected_score

    def __call__(self, game: Game) -> float:
        return self.evaluator(game)


def eval_checkers_1(game: CheckersGame, depth=None) -> int:
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

def eval_othello_1(game: OthelloGame, depth=None) -> int:
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

def __win_connect4(num: int, last_move_player: str, depth: int) -> float:
    score = connect4_depth_affected_score(num, depth)
    if last_move_player != BLACK:
        return score * -1
    return score

def connect4_depth_affected_score(score: float, depth: int) -> float:
    return score / max(depth, 1)

def connect4_get_unaffected_score(score: float, depth: int) -> float:
    return score * depth

def __check_win_connect4(game: Connect4, depth: int):
    max_rows, max_cols = game.getDimensions()

    board_copy = game.getBoardCopy()
    board = np.array(board_copy, dtype=np.chararray)
    last_move_col = game.getMoveHist()

    if len(last_move_col) < 7:
        return 0 # Not enough moves played to win

    actual_move = last_move_col[-1]
    row, col = np.min(np.where(board[actual_move] != NONE)), actual_move
    last_move_player = board[col][row]

    col_safe = max(0, col - 4)
    winner = 0
    # print(row, col)
    if row < max_rows - 3:
        vert_check = np.all(board[col, row:(row+4)] == last_move_player)
        if vert_check:
            # print('win vert', last_move_player)
            # print(board[col, row:(row+3)])
            return __win_connect4(1, last_move_player, depth)

    player_moves_in_row = np.where(board[:, row] == last_move_player)[0]
    if len(player_moves_in_row) >= 4:
        for c in range(player_moves_in_row[0], max_cols - 3):
            row_check = np.all(board[c:(c+4), row] == last_move_player)
            # print(board[c:(c+4), row] == last_move_player)
            if row_check:
                # print('win row', last_move_player)
                # print(board[c:(c+3), row])
                return __win_connect4(1, last_move_player, depth)

    lines = (
        diagonalsPos(board, max_cols, max_rows),  # positive diagonals
        diagonalsNeg(board, max_cols, max_rows)  # negative diagonals
    )
    for line in chain(*lines):
        for color, group in groupby(line):
            if color != NONE and len(list(group)) >= 4:
                return __win_connect4(1, color, depth)
    
    return 0


def eval_connect4_1(game: Connect4, depth=1) -> int:
    return __check_win_connect4(game, depth)


def eval_c4pop10_1(game: C4Pop10Game) -> int:
    redScore = game.getRedScore()
    yellowScore = game.getYellowScore()

    score = 0

    score += redScore.safeDisks * 100
    score += redScore.threatDisks * 50
    score += redScore.keptDisks * 120

    score -= yellowScore.safeDisks * 100
    score -= yellowScore.threatDisks * 50
    score -= yellowScore.keptDisks * 120

    if game.getWhoseMove() == "RED":
        score += 50
    else:
        score -= 50
    
    return score

try:
    from tictactoe import TicTacToeGame
    def eval_tic_tac_toe_1(game: TicTacToeGame) -> int:
        winner = game.getWinner()
        if winner is None:
            print(game.showBoard())
        assert winner is not None
        if winner == "max":
            return 1
        elif winner == "min":
            return -1
        else:
            return 0
except ModuleNotFoundError:
    TicTacToeGame = None
    eval_tic_tac_toe_1 = None

_num_rollouts = 2
def eval_random_rollout(game: Game) -> int:
    score = 0
    key = game.getBoardKey()
    for _ in range(_num_rollouts):
        winner = game.getWinner()
        count = 0
        while winner is None:
            game.doMove(random.choice(game.getValidMoves()))
            count += 1
            winner = game.getWinner()
        game.undoMoves(count)
        if winner == 'max':
            score += 1
        elif winner == 'min':
            score -= 1
    assert key == game.getBoardKey()
    return score
