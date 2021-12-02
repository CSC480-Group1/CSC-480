#! /usr/bin/env python3
from itertools import groupby, chain

NONE = '.'
BLACK = 'B'
WHITE = 'W'


def diagonalsPos(matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]


def diagonalsNeg(matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]


class Connect4Impl:
    def __init__(self, cols=7, rows=6, requiredToWin=4):
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        self.turn = BLACK
        self.board = [[NONE] * rows for _ in range(cols)]
        self.game_over = False

    def reset_game(self):
        self.turn = BLACK
        self.board = [[NONE] * self.rows for _ in range(self.cols)]
        self.game_over = False

    def insert(self, column, shadow=False):
        color = self.turn
        c = self.board[column]
        if c[0] != NONE:
            if not shadow:
                self.printBoard()
                print(f'Column {column} is full')
            return False

        i = -1
        while c[i] != NONE:
            i -= 1

        if not shadow:
            c[i] = color

            have_won = self.checkForWin()
            if have_won:
                self.game_over = True
            else:
                self.turn = WHITE if self.turn == BLACK else BLACK
        return True


    def getWhoseMove(self):
        return 'BLACK' if self.turn == BLACK else 'WHITE'


    def checkForWin(self):
        w = self.getWinner()
        return w
        """ if w:
            self.printBoard()
            # raise Exception(w + ' won!')
            print(w + ' won!') """


    def getWinner(self):
        lines = (
            self.board,  # columns
            zip(*self.board),  # rows
            diagonalsPos(self.board, self.cols, self.rows),  # positive diagonals
            diagonalsNeg(self.board, self.cols, self.rows)  # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != NONE and len(list(group)) >= self.win:
                    return color

    @staticmethod
    def getRepr(board, rows, cols):
        string = '   ' + '  '.join(map(str, range(cols))) + '\n'
        for y in range(rows):
            string += '  '.join([str(y)] + [str(board[x][y]) for x in range(cols)]) + '\n'

        return string

    def getBoardRepr(self):
        return Connect4Impl.getRepr(self.board, self.rows, self.cols)

    def printBoard(self):
        print(self.getBoardRepr())

    def getValidMoves(self):
        if self.game_over:
            return []

        valid_moves = list(filter(lambda col: self.insert(col, shadow=True), range(self.cols)))
        for c in range(self.cols):
            success = self.insert(c, shadow=True)
        
        return valid_moves


if __name__ == '__main__':
    g = Connect4Impl()
    while True:
        g.printBoard()
        row = input('{}\'s turn: '.format(g.getWhoseMove()))
        g.insert(int(row))
