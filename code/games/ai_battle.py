from Player import MinimaxPlayer, MonteCarloPlayer, Player, RandomPlayer
import eval_funcs
from Games import *
import time
from itertools import combinations

import datetime
from pathlib import Path
import csv

import sys

"""

This file contains classes to battle AI agents against each other.

Information about how to use these classes can be found in the README.

Demo for usage of this file: https://colab.research.google.com/drive/1qbrKeExzzBb-K7HgdM5KGTJri61nlGLZ?usp=sharing

"""

try:
    from tictactoe import TicTacToeGame
except ModuleNotFoundError:
    TicTacToeGame = None

has_tqdm = True
try:
    import tqdm
except ModuleNotFoundError:
    has_tqdm = False

class NoTQDMException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidGameException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AllPlayerBattle:
    """
    Class for running match-ups of given players. Each given player plays each other
    in the given game choice and outputs the results as either a CSV or object.

    Information about how to use this can be found in the README.
    """
    def __init__(self, game_choice, write_to_csv=True, move_limit=300, play_count=5,
            players=None, use_tqdm=True) -> None:
        if use_tqdm and not has_tqdm:
            raise NoTQDMException('TQDM is not installed: <python3 -m pip install tqdm>')
        self.use_tqdm = use_tqdm

        self.move_limit = move_limit
        self.play_count = play_count
        self.write_to_csv = write_to_csv
        self.writer = None
        self.pbar = None
        self.game_choice = game_choice
        self.game = None
        self.game_class = AllPlayerBattle.parse_game_type(game_choice)
        if isinstance(game_choice, Game):
            self.game = game_choice

        self.players = players
        if self.players is None:
            self.players = AllPlayerBattle.get_default_players(self.game_class)

        assert len(self.players) > 1

        self.game_matchups = AllPlayerBattle.generate_player_matchups(self.players)

        if self.write_to_csv:
            self.writer = CSVGameWrite(self.game_class.__name__)

    @staticmethod
    def parse_game_type(game_choice):
        if isinstance(game_choice, str):
            return AllPlayerBattle.get_game_from_choice(game_choice)
        elif isinstance(game_choice, Game):
            return type(game_choice)
        elif game_choice in AllPlayerBattle.get_game_choice_map().values():
            return game_choice

        raise Exception(f'Invalid type for game_choice: {type(game_choice)}')

    @staticmethod
    def get_game_choice_map():
        games = {
            "checkers": CheckersGame,
            "othello": OthelloGame,
            "c4pop10": C4Pop10Game,
            "connect4": Connect4
        }

        if TicTacToeGame is not None:
            games["tic tac toe"] = TicTacToeGame

        return games

    @staticmethod
    def get_default_players(game_class):
        defaults = {
            CheckersGame: [
                MinimaxPlayer(eval_funcs.EvalFnGuide.get_default_fn_for_game(CheckersGame), 6),
                MonteCarloPlayer(num_iter=500, c=1.414)
            ],
            OthelloGame: [
                MinimaxPlayer(eval_funcs.EvalFnGuide.get_default_fn_for_game(OthelloGame), 4),
                MonteCarloPlayer(num_iter=500, c=1.414)
            ],
            C4Pop10Game: [
                MinimaxPlayer(eval_funcs.EvalFnGuide.get_default_fn_for_game(C4Pop10Game), 6),
                MonteCarloPlayer(num_iter=500, c=1.414)
            ],
            TicTacToeGame: [
                MinimaxPlayer(eval_funcs.EvalFnGuide.get_default_fn_for_game(TicTacToeGame), 9),
                MonteCarloPlayer(num_iter=500, c=1.414)
            ],
            Connect4: [
                MinimaxPlayer(eval_funcs.EvalFnGuide.get_default_fn_for_game(Connect4), 4),
                MonteCarloPlayer(num_iter=500, c=1.414)
            ]
        }

        for g in defaults:
            defaults[g].append(RandomPlayer())

        return defaults[game_class]

    @staticmethod
    def generate_player_matchups(players):
        return list(combinations(players, 2))

    @staticmethod
    def get_game_from_choice(game_choice: str):
        game_map = AllPlayerBattle.get_game_choice_map()
        g = game_map.get(game_choice)

        if g is None:
            raise InvalidGameException('Valid games include: {}'.format(
                ', '.join([f'"{game_str}"' for game_str in AllPlayerBattle.get_game_choice_map().keys()])
            ))

        return g

    def __update_res(self, res):
        if self.use_tqdm:
            self.pbar.update()
        if self.writer is not None:
            self.writer.write_result(res)
        else:
            print(res)

    def get_game_class(self):
        return self.game_class

    def battle(self, suppress_output=True):
        """Actually runs the matchups"""
        # Setup
        if self.game is None:
            self.game = self.game_class()
        game = self.game
        if self.writer is not None:
            self.writer.open()
        if self.use_tqdm and not self.pbar:
            self.pbar = tqdm.tqdm(total=(len(self.game_matchups) * 2 * self.play_count), desc='Simulating games')

        results = []
        def add_results_and_update(res):
            results.append(res)
            self.__update_res(res)

        print("Playing", game.__class__.__name__)
        for p1, p2 in self.game_matchups:
            new_battle = AIBattle(game, p1, p2, update=add_results_and_update,
                move_limit=self.move_limit, play_count=self.play_count)
            new_battle.go()

        if self.writer is not None:
            self.writer.close()

        if self.use_tqdm:
            self.pbar.close()

        if not suppress_output:
            return results

class MinimaxMonteCarloRandomPlayerBattle(AllPlayerBattle):
    """
    Class to play a MCTS, Minimax, and RandomPlayer agent all against each other using the AllPlayerBattle.

    Allows you to specify the arguments for MCTS and Minimax players directly.
    """
    def __init__(self, game_choice,
            minimax_depth=None, minimax_eval_fn=None,
            monte_carlo_c=None, monte_carlo_iters=None,
            **kwargs) -> None:
        game_c = AllPlayerBattle.parse_game_type(game_choice)
        default_players = AllPlayerBattle.get_default_players(game_c)

        minimax_player: MinimaxPlayer = next(filter(lambda p: isinstance(p, MinimaxPlayer), default_players), None)
        monte_carlo_player: MonteCarloPlayer = next(filter(lambda p: isinstance(p, MonteCarloPlayer), default_players), None)
        random_player: RandomPlayer = next(filter(lambda p: isinstance(p, RandomPlayer), default_players), None)

        if minimax_player is None or monte_carlo_player is None or random_player is None:
            raise Exception(f'Not all 3 expected player types are supported as default players for {game_choice}!')

        if minimax_depth is not None:
            minimax_player.set_depth_limit(minimax_depth)
        if minimax_eval_fn is not None:
            minimax_player.set_eval_func(minimax_eval_fn)

        if monte_carlo_c is not None:
            monte_carlo_player.set_c(monte_carlo_c)
        if monte_carlo_iters is not None:
            monte_carlo_player.set_num_iter(monte_carlo_iters)

        super().__init__(game_choice, players=[minimax_player, monte_carlo_player, random_player], **kwargs)

class AIBattle:
    """
    Class to run a single matchup between 2 players. Call `go()` to run the matchup.
    """
    def __init__(self, game: Game, p1: Player, p2: Player, update=print, move_limit=300, play_count=5) -> None:
        self.p1 = p1
        self.p2 = p2
        self.game = game
        self.update = update
        self.move_limit = move_limit
        self.play_count = play_count

    def go(self):
        print(str(self.p1), "vs.", str(self.p2))
        for _ in range(self.play_count):
            result = self.__play_game(self.p1, self.p2)
            self.update(result)
        for _ in range(self.play_count):
            result = self.__play_game(self.p2, self.p1)
            self.update(result)

    def __play_game(self, maxPlayer, minPlayer):
        return AIBattle._play_game(self.game, self.move_limit, maxPlayer, minPlayer)

    @staticmethod
    def _play_game(game, move_limit, maxPlayer, minPlayer):
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

class CSVGameWrite:
    """
    Class to write the game results to a CSV file.
    """
    def __init__(self, game_name: str, data_dir='.',
            field_names=['game', 'max', 'min', 'winner', 'max_tottime', 'min_tottime', 'move_count']) -> None:
        self.datafile = Path('{}/data-{}-{}.csv'.format(data_dir, game_name, datetime.datetime.now().strftime('%m_%d-%H_%M')))
        self.writer = None
        self.file = None
        self.field_names = field_names
        self.wrote_header = False

    def open(self):
        if self.file is None:
            df = self.datafile.open('w')
            self.file = df
            writer = csv.DictWriter(df, fieldnames=self.field_names)
            self.writer = writer

    def write_result(self, row):
        if self.writer is None:
            raise Exception('Writer must first be opened!')

        if not self.wrote_header:
            self.wrote_header = True
            self.writer.writeheader()

        self.writer.writerow(row)

    def close(self):
        if self.file:
            self.file.close()
            self.file = None
            self.writer = None
            self.wrote_header = False


if __name__ == "__main__":
    """If exec-ed from the command line, just play a default AllPlayerBattle with
    MCTS, Minimax, and RandomPlayer with the given game"""
    if len(sys.argv) < 2:
        print("No game specified")
        exit(1)

    if TicTacToeGame is None and sys.argv[1] == "tic tac toe":
        print("Tic tac toe requires numpy, install with <python3 -m pip install numpy>")
        exit(1)

    all_battles = AllPlayerBattle(sys.argv[1])

    all_battles.battle()
