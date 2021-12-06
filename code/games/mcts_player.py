from typing import Type
from Games import *
from BoardTest import getBoardValue
from Player import MonteCarloPlayer
from interactive_agent import InteractiveAgent, InteractiveGameRunner
from mcts import mcts
import argparse
try:
    from tictactoe import TicTacToeGame
except ModuleNotFoundError:
    TicTacToeGame = None


"""

This file contains the classes needed to play against a MCTS agent from either the
object InteractiveMCTSGame or InteractiveMCTSGameRunner.

InteractiveMCTSGameRunner allows running against the mcts agent from the command line.

"""

class InteractiveMCTSGame(InteractiveAgent):
    def __init__(self, game, user_playing_as=None, player: MonteCarloPlayer=None) -> None:
        super().__init__(game, user_playing_as, player)
        self.player: MonteCarloPlayer = self.player

    @staticmethod
    def get_player_type():
        return MonteCarloPlayer

    def on_possible_user_move(self, move_number, move):
        return print("  {}) {}".format(move_number+1, move))

    def do_ai_agent_move(self):
        game = self.game
        player = game.getPlayer()
        startkey = game.getBoardKey()
        move = mcts(game, player, self.player.get_num_iters(), c=self.player.get_c())
        assert game.getBoardKey() == startkey
        print("MCTS plays {}".format(move))
        game.doMove(move)

    def show_winner(self):
        winner = self.game.getWinner()
        if winner == 'draw':
            print('Draw!')
        else:
            print("{} wins!".format(winner))

class InteractiveMCTSGameRunner(InteractiveGameRunner):
    def __init__(self) -> None:
        super().__init__()

    def get_interactive_game_str(self):
        return 'mcts'

    def add_optional_args(self, parser: argparse.ArgumentParser):
        """Can override the number of iterations MCTS does and what the exploration parameter is"""
        parser.add_argument('--num-iters', '-n', metavar='iterations', type=int, required=False, help="MCTS iterations")
        parser.add_argument('--c', '-c', metavar='c', required=False, type=float, help="C value")

    def player_setup(self, parsed_args, game_class: Type[Game], player: MonteCarloPlayer):
        if parsed_args.num_iters:
            player.set_num_iter(parsed_args.num_iters)
        if parsed_args.c:
            player.set_c(parsed_args.c)

    def get_interactive_game(self):
        return InteractiveMCTSGame

    def get_playing_opts_str(self, player: MonteCarloPlayer) -> str:
        return f"iterations = {player.get_num_iters()} and c = {player.get_c()}"

if __name__ == "__main__":
    """If run from the command line, use command line parser class"""
    InteractiveMCTSGameRunner().go()