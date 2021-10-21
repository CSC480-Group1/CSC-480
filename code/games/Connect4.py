#! /usr/bin/env python3
from itertools import groupby, chain

NONE = '.'
RED = 'R'
YELLOW = 'Y'


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
        self.turn = RED
        self.board = [[NONE] * rows for _ in range(cols)]

    def insert(self, column, shadow=False):
        color = self.turn
        c = self.board[column]
        if c[0] != NONE:
            print('Column is full')
            return False

        i = -1
        while c[i] != NONE:
            i -= 1

        if not shadow:
            c[i] = color

            self.checkForWin()
            self.turn = YELLOW if self.turn == RED else RED
        return True


    def getWhoseMove(self):
        return 'Red' if self.turn == RED else 'Yellow'


    def checkForWin(self):
        w = self.getWinner()
        if w:
            self.printBoard()
            raise Exception(w + ' won!')


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


    def printBoard(self):
        print('   ' + '  '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print('  '.join([str(y)] + [str(self.board[x][y]) for x in range(self.cols)]))
        print()


    def getValidMoves(self):
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
