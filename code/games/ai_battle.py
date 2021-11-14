from abc import ABC, abstractmethod
import random
import minimax
import eval_funcs
import mcts
from Games import *


class Player(ABC):
    @abstractmethod
    def play(self, game: Game):
        pass

class MonteCarloPlayer(Player):
    def play(self, game: Game):
        move = mcts.mcts(game, game.getPlayer(), 300)
        print("Mcts plays {}".format(move))
        game.doMove(move)

class MinimaxPlayer(Player):
    def __init__(self, eval_func, depth_limit=6):
        self._eval_func = eval_func
        minimax.set_depth_limit(depth_limit)

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

game = C4Pop10Game()
maxPlayer = MonteCarloPlayer()
minPlayer = MinimaxPlayer(eval_funcs.eval_c4pop10_1)
# player2 = RandomPlayer()

while True:
    print(game.showBoard())
    if len(game.getValidMoves()) == 0:
        break
    maxPlayer.play(game)

    print(game.showBoard())
    if len(game.getValidMoves()) == 0:
        break
    minPlayer.play(game)

val = game.getWinner()

if val == "max":
    print("{} wins!".format(maxPlayer.__class__.__name__))
elif val == "min":
    print("{} wins!".format(minPlayer.__class__.__name__))
else:
    print("Draw!")

