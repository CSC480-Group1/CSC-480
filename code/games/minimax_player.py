from Games import *
from Player import MinimaxPlayer, Player
from ai_battle import AllPlayerBattle
from eval_funcs import *
from interactive_agent import InteractiveAgent, InteractiveGameRunner, InteractivePlayerHelper
from minimax import *
import argparse

class InteractiveMinimaxGame(InteractiveAgent):
    def __init__(self, game: Game, user_playing_as=None, player: MinimaxPlayer=None) -> None:
        super().__init__(game, user_playing_as, player)
        self.player: MinimaxPlayer = self.player

    @staticmethod
    def get_player_type():
        return MinimaxPlayer

    def on_possible_player_move(self, move_number, move):
        self.game.doMove(move)
        val = minimax_val(self.game, self.player.get_eval_func(), float('-inf'), float('inf'), self.player.get_depth_limit())
        self.game.undoMoves(1)
        print("  {}) {} ({})".format(move_number+1, move, val))

    def show_winner(self):
        final_score = self.player.get_eval_func()(self.game)

        if final_score == 0:
            print("Draw!")
        elif final_score > 0:
            print("Max wins!")
        else:
            print("Min wins!")

    def do_ai_agent_move(self) -> None:
        move = minimax_best_move(self.game, eval_fn=self.player.get_eval_func(), depth_limit=self.player.get_depth_limit())
        print("Minimax plays {}".format(move))
        self.game.doMove(move)


class InteractiveMinimaxGameRunner(InteractiveGameRunner):
    def __init__(self) -> None:
        super().__init__()

    def get_interactive_game_str(self):
        return 'minimax'

    def add_optional_args(self, parser: argparse.ArgumentParser):
        parser.add_argument('--depth-limit', '-d', metavar='depth', type=int, required=False, help="Game depth limit")
        parser.add_argument('--eval-fn', '-e', metavar='fn_name', required=False, help="Evaluation function")

    def player_setup(self, parsed_args, game_class: Type[Game], player: MinimaxPlayer):
        if parsed_args.depth_limit:
            player.set_depth_limit(parsed_args.depth_limit)
        if parsed_args.eval_fn:
            player.set_eval_func(EvalFnGuide.get_eval_fn_from_str(game_class, parsed_args.eval_fn))

    def get_interactive_game(self):
        return InteractiveMinimaxGame

    def get_playing_opts_str(self, player: MinimaxPlayer) -> str:
        return f"eval_fn = {player.get_eval_func()} and depth limit = {player.get_depth_limit()}"

if __name__ == "__main__":
    InteractiveMinimaxGameRunner().go()