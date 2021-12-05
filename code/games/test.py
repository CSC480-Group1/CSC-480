# from ai_battle import *
# from eval_funcs import *
# from Games import *
# from tictactoe import TicTacToeGame
from Games import Game, CheckersGame, C4Pop10Game, OthelloGame, Connect4
from tictactoe import TicTacToeGame
import gc

g = Connect4()
print(g.getMoveHist())
g.close()
g.getMoveHist()
g = TicTacToeGame()
print('here')