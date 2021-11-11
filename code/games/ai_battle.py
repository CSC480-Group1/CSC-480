from abc import ABC, abstractmethod
import random
import minimax
import eval_funcs
import mcts
from Games import *
from BoardTest import getBoardValue


class Player(ABC):
    @abstractmethod
    def play(self, game: Game):
        pass

class MonteCarloPlayer(Player):
    def play(self, game: Game):
        move = mcts.mcts(game, game.getPlayer())
        print("Mcts plays {}".format(move))
        game.doMove(move)

class MinimaxPlayer(Player):
    def __init__(self, eval_func):
        self._eval_func = eval_func
        minimax.set_depth_limit(3)

    def play(self, game: Game):
        move = minimax.minimax_best_move(game, self._eval_func)
        print("Minimax plays {}".format(move))
        game.doMove(move)

class RandomPlayer(Player):
    def play(self, game: Game):
        moves = game.getValidMoves()
        assert len(moves) > 0
        move = random.choice(moves)
        print("Random plays {}".format(move))
        game.doMove(move)

game = OthelloGame()
player1 = MonteCarloPlayer()
player2 = MinimaxPlayer(eval_funcs.eval_othello_1)
# player2 = RandomPlayer()

while True:
    print(game.showBoard())
    if len(game.getValidMoves()) == 0:
        break
    player1.play(game)

    print(game.showBoard())
    if len(game.getValidMoves()) == 0:
        break
    player2.play(game)

val = getBoardValue()

if val > 0:
    print("Black wins!")
elif val < 0:
    print("White wins!")
else:
    print("Draw!")

