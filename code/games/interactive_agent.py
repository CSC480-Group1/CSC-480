from abc import ABC, abstractmethod
from typing import Type
from Games import *
from Player import Player
from ai_battle import AllPlayerBattle
from tictactoe import TicTacToeGame
import argparse
import sys

class InteractiveAgent(ABC):
    def __init__(self, game: Game, user_playing_as=None, player=None, **game_kwargs) -> None:
        self.game = game
        self.user_playing_as = user_playing_as
        if player is None:
            self.player = InteractivePlayerHelper.get_default_player(type(game), self.get_player_type())
        else:
            self.player = player

    @abstractmethod
    def on_possible_player_move(self, move_number, move):
        pass

    @abstractmethod
    def do_ai_agent_move(self):
        pass

    @abstractmethod
    def show_winner(self):
        pass

    @abstractmethod
    def get_player_type(self) -> Type[Player]:
        pass

    def _get_who_user_will_play(self):
        self.user_playing_as = InteractiveAgent.get_who_user_will_play()

    def play(self):
        if self.user_playing_as is None:
            self._get_who_user_will_play()
        self.run_game()

    def print_board(self):
        print("\n\n")
        print(self.game.showBoard())

    def try_play(self, play_fn):
        self.print_board()
        play_fn()

    def run_game(self):
        if self.user_playing_as == "max":
            self.try_play(self.doPlayerPlay)

        curr_play = self.do_ai_agent_move

        while self.game.getWinner() is None:
            self.try_play(curr_play)
            if self.user_playing_as != "n":
                if curr_play == self.do_ai_agent_move:
                    curr_play = self.doPlayerPlay
                else:
                    curr_play = self.do_ai_agent_move

        self.print_board()
        self.show_winner()

    @staticmethod
    def get_who_user_will_play():
        print("Play as max or min? (n for no player)")
        options = ["max", "min", "n"]
        while True:
            response = input(f"({'/'.join(options)})> ")
            if response in options:
                return response
            else:
                print(f"Enter {' or '.join(options)}")

    def doPlayerPlay(self) -> None:
        game = self.game
        moves = game.getValidMoves()
        if len(moves) == 0:
            return
        print("Possible moves:")
        for i, move in enumerate(moves):
            self.on_possible_player_move(i, move)

        move = ""

        while True:
            choice = input('> ')
            try:
                if choice == 'q':
                    raise Exception("Stop game")
                choice = int(choice)
                if choice > 0 and choice <= len(moves):
                    move = moves[choice-1]
                    break
                print("Enter a number between 1 and {}".format(len(moves)))
            except ValueError:
                print("Enter an integer")

        game.doMove(move)

class InteractivePlayerHelper:
    @staticmethod
    def get_game_options():
        game_options = ['Checkers', 'Othello', 'Connect4', 'C4Pop10']
        if TicTacToeGame is not None:
            game_options.append('Tic Tac Toe')

        return game_options

    @staticmethod
    def get_game():
        game_options = InteractivePlayerHelper.get_game_options()
        print("Game options:")
        for i, opt in enumerate(game_options):
            print(f"  {i+1}) {opt}")

        while True:
            response = input('> ')
            if response == '1':
                game = CheckersGame
                break
            elif response == '2':
                game = OthelloGame
                break
            elif response == '3':
                game = Connect4
                break
            elif response == '3':
                game = C4Pop10Game
                break
            elif TicTacToeGame is not None and response == '5':
                game = TicTacToeGame
                break
            print("Choices are " + ', '.join([f"'{i+1}'" for i in range(len(game_options))]))

        return game

    @staticmethod
    def get_default_player(game_class: Type[Game], PlayerType: Type[Player]):
        default_players = AllPlayerBattle.get_default_players(game_class=game_class)
        default_player = next(filter(lambda p: isinstance(p, PlayerType), default_players), None)
        if default_player is None:
            raise Exception(f'No default players found for {game_class}')

        return default_player

class InteractiveGameRunner(ABC):
    def __init__(self) -> None:
        self.game_class: Type[Game] = None
        self._player: Player = None
        self.game_options = InteractivePlayerHelper.get_game_options()

    @abstractmethod
    def add_optional_args(self, parser: argparse.ArgumentParser):
        pass

    @abstractmethod
    def player_setup(self, args, game_class: Type[Game], player: Player):
        pass

    @abstractmethod
    def get_interactive_game_str(self):
        pass

    @staticmethod
    @abstractmethod
    def get_interactive_game() -> Type[InteractiveAgent]:
        pass

    @abstractmethod
    def get_playing_opts_str(self, player: Player) -> str:
        pass

    def go(self):
        if len(sys.argv) > 1:
            parsed_args = self.__get_parsed_args()

            if parsed_args.game is None:
                self.game_class = InteractivePlayerHelper.get_game()
            else:
                self.game_class = AllPlayerBattle.get_game_from_choice(parsed_args.game.lower())
            self._player = self.__setup_default_player()
            self.player_setup(parsed_args, self.game_class, self._player)
        else:
            self.game_class = InteractivePlayerHelper.get_game()
            self._player = self.__setup_default_player()

        self.__run_interactive_game()

    def __get_parsed_args(self):
        parser = argparse.ArgumentParser(
            description=f'Run interactive {self.get_interactive_game_str()} game as player or watch agents battle.'
        )
        parser.add_argument('--game', '-g', metavar='game', help="Which game. Options: {}".format(
            ', '.join([f'"{game_str}"' for game_str in self.game_options])
        ), required=False)

        self.add_optional_args(parser)

        return parser.parse_args()

    def __setup_default_player(self):
        assert self.game_class is not None
        player_type = self.get_interactive_game().get_player_type()
        return InteractivePlayerHelper.get_default_player(self.game_class, player_type)

    def __run_interactive_game(self):
        assert self.game_class is not None
        print(f'\nPlaying {self.game_class} with {self.get_playing_opts_str(self._player)}\n')
        self.get_interactive_game()(self.game_class(), player=self._player).play()


