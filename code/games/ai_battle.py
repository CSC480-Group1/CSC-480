from abc import ABC, abstractmethod
import random
import minimax
import eval_funcs
import mcts
from Games import *
import time

import datetime
from pathlib import Path
import csv

import sys

try:
    from tictactoe import TicTacToeGame
except ModuleNotFoundError:
    TicTacToeGame = None

has_tqdm = True
try:
    import tqdm
except ModuleNotFoundError:
    has_tqdm = False


class Player(ABC):
    @abstractmethod
    def play(self, game: Game):
        pass

class MonteCarloPlayer(Player):
    def __init__(self, num_iter = 300):
        self._num_iter = num_iter
    
    def play(self, game: Game):
        move = mcts.mcts(game, game.getPlayer(), self._num_iter, quiet=True)
        #print("Mcts plays {}".format(move))
        game.doMove(move)
    
    def __str__(self):
        return "{}(num_iter={})".format(self.__class__.__name__, self._num_iter)

class MinimaxPlayer(Player):
    def __init__(self, eval_func, depth_limit=6):
        self._eval_func = eval_func
        self._depth_limit = depth_limit
        minimax.set_depth_limit(depth_limit)

        self._tt = {}

    def play(self, game: Game):
        move = minimax.minimax_best_move(game, self._eval_func, quiet=True, tt=self._tt)
        #print("Minimax plays {}".format(move))
        game.doMove(move)
    
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

move_limit = 300
def play_game(game, maxPlayer, minPlayer):
    moveCount = 0
    max_tottime = min_tottime = 0
    while True:
        moveCount += 1
        if moveCount == move_limit:
            print("Hit move limit")
            break
        if game.getWinner() is not None:
            break
        timer = time.perf_counter()
        maxPlayer.play(game)
        max_tottime += time.perf_counter() - timer

        if game.getWinner() is not None:
            break
        timer = time.perf_counter()
        minPlayer.play(game)
        min_tottime += time.perf_counter() - timer

    winner = game.getWinner()
    game.undoMoves(len(game.getMoveHist()))
    return {
        'game': game.__class__.__name__,
        'max': str(maxPlayer),
        'min': str(minPlayer),
        'winner': winner,
        'max_tottime': max_tottime,
        'min_tottime': min_tottime,
        'move_count': moveCount
    }

games = {
    "checkers": (CheckersGame, eval_funcs.eval_checkers_1, 4),
    "othello": (OthelloGame, eval_funcs.eval_othello_1, 4),
    "c4pop10": (C4Pop10Game, eval_funcs.eval_c4pop10_1, 6)
}

if TicTacToeGame is not None:
    games["tic tac toe"] = (TicTacToeGame, eval_funcs.eval_tic_tac_toe_1, 9)

if len(sys.argv) < 2:
    print("No game specified")
    exit(1)

if TicTacToeGame is None and sys.argv[1] == "tic tac toe":
    print("Tic tac toe requires numpy")
    exit(1)

if sys.argv[1] not in games:
    print("Unknown game {}".format(sys.argv[1]))
    exit(1)

gameOpts = games[sys.argv[1]]

pairs = [
    (MinimaxPlayer(gameOpts[1], gameOpts[2]), RandomPlayer()),
    (MinimaxPlayer(eval_funcs.eval_random_rollout, gameOpts[2]), RandomPlayer()),
    (MinimaxPlayer(gameOpts[1], gameOpts[2]), MinimaxPlayer(eval_funcs.eval_random_rollout, gameOpts[2]))
]
play_count = 5

game = gameOpts[0]()

dataFile = Path('./data-{}-{}.csv'.format(sys.argv[1], datetime.datetime.now().strftime('%m_%d-%H_%M')))

print("Playing", game.__class__.__name__)

if has_tqdm:
    pbar = tqdm.tqdm(total=(len(pairs) * 2 * play_count), desc='Simulating games')


with dataFile.open('w') as df:
    writer = csv.DictWriter(df, fieldnames=['game', 'max', 'min', 'winner', 'max_tottime', 'min_tottime', 'move_count'])
    writer.writeheader()
    try:
        for pair in pairs:
            print(str(pair[0]), "vs.", str(pair[1]))
            for _ in range(play_count):
                result = play_game(game, pair[0], pair[1])
                writer.writerow(result)
                if has_tqdm:
                    pbar.update()
            for _ in range(play_count):
                result = play_game(game, pair[1], pair[0])
                writer.writerow(result)
                if has_tqdm:
                    pbar.update()
    except KeyboardInterrupt:
        print("Interrupted!")

if has_tqdm:
    pbar.close()

