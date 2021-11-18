import numpy as np
import random
from Games import Game

def _next_player(player: str) -> str:
    if player == 'max':
        return 'min'
    elif player == 'min':
        return 'max'
    else:
        raise ValueError('Unknown Player "{}"'.format(player))

class TicTacToeGame(Game):

    def _get_player_letter(self):
        if self._curr_player == 'max':
            return 'X'
        elif self._curr_player == 'min':
            return 'O'
        else:
            raise ValueError('Unknown player "{}"'.format(self._curr_player))

    def __init__(self):
        self._board = np.full( (3, 3), ' ')
        self._move_hist = []
        self._curr_player = 'max'

    def doMove(self, move: str):
        move = int(move) - 1
        assert not move in self._move_hist
        self._board.flat[move] = self._get_player_letter()
        self._curr_player = _next_player(self._curr_player)
        self._move_hist.append(move)

    def undoMoves(self, movecount: int):
        for _ in range(min(movecount, len(self._move_hist))):
            move = self._move_hist[-1]
            self._move_hist = self._move_hist[:-1]
            self._curr_player = _next_player(self._curr_player)
            assert self._board.flat[move] == self._get_player_letter()
            self._board.flat[move] = ' '

    def getBoardKey(self):
        return ''.join(self._board.flat)

    def showBoard(self):
        out = ""
        for row in self._board:
            for col in row:
                out += "{} ".format(col if col != " " else ".")
            out += "\n"
        out += "{}'s turn".format(self._get_player_letter())
        return out

    def getValidMoves(self):
        if self.getWinner() is not None:
            return []
        moves = []
        for i, spot in enumerate(self._board.flat):
            if spot == " ":
                moves += str(i+1)
        return moves

    def getMoveHist(self):
        return [str(move + 1) for move in self._move_hist]

    def getPlayer(self):
        return self._curr_player

    def getWinner(self):
        if np.any(np.all(self._board == 'X', axis=0)) or \
            np.any(np.all(self._board == 'X', axis=1)) or \
            np.all(self._board.diagonal() == 'X') or \
            np.all(np.fliplr(self._board).diagonal() == 'X'):
                return 'max'
        elif np.any(np.all(self._board == 'O', axis=0)) or \
            np.any(np.all(self._board == 'O', axis=1)) or \
            np.all(self._board.diagonal() == 'O') or \
            np.all(np.fliplr(self._board).diagonal() == 'O'):
                return 'min'
        elif not (self._board == ' ').any():
            return 'draw'
        else:
            return None
