from abc import ABC, abstractmethod
import random
from Games import Game
import minimax
import mcts

class Player(ABC):
    @abstractmethod
    def play(self, game: Game):
        pass

class MonteCarloPlayer(Player):
    def __init__(self, num_iter = 300, c=1):
        self._num_iter = num_iter
        self._c = c
    
    def play(self, game: Game):
        move = mcts.mcts(game, game.getPlayer(), self._num_iter, quiet=True, c=self._c)
        #print("Mcts plays {}".format(move))
        game.doMove(move)

    def set_num_iter(self, num_iter):
        self._num_iter = num_iter

    def set_c(self, c):
        self._c = c
    
    def __str__(self):
        return "{}(num_iter={},c={})".format(self.__class__.__name__, self._num_iter, self._c)

class MinimaxPlayer(Player):
    def __init__(self, eval_func, depth_limit=6):
        self._eval_func = eval_func
        self._depth_limit = depth_limit

    def play(self, game: Game):
        move = minimax.minimax_best_move(game, self._eval_func, quiet=True, depth_limit=self._depth_limit)
        #print("Minimax plays {}".format(move))
        game.doMove(move)

    def set_depth_limit(self, depth_limit):
        self._depth_limit = depth_limit

    def set_eval_func(self, eval_func):
        self._eval_func = eval_func

    def get_depth_limit(self):
        return self._depth_limit

    def get_eval_func(self):
        return self._eval_func
    
    def __str__(self):
        return "{}(eval_func={},depth_limit={})".format(self.__class__.__name__, self._eval_func.__name__, self._depth_limit)

class RandomPlayer(Player):
    def play(self, game: Game):
        moves = game.getValidMoves()
        assert len(moves) > 0
        move = random.choice(moves)
        #print("Random plays {}".format(move))
        game.doMove(move)
    
    def __str__(self):
        return self.__class__.__name__