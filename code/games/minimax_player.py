from Games import *
from eval_funcs import *
from minimax import *

class InteractiveMinimaxGame:
    def __init__(self, game, eval_fn, user_playing_as=None, depth_limit=5) -> None:
        self.game = game
        self.eval_fn = eval_fn
        self.depth_limit = depth_limit
        self.user_playing_as = user_playing_as

    def _do_player_play(self):
        InteractiveMinimaxGame.doPlayerPlay(self.game, self.eval_fn, self.depth_limit)

    def _do_minimax_play(self):
        InteractiveMinimaxGame.doMinimaxPlay(self.game, self.eval_fn, self.depth_limit)

    def _get_who_user_will_play(self):
        self.user_playing_as = InteractiveMinimaxGame.get_who_user_will_play()

    def play(self):
        if self.user_playing_as is None:
            self._get_who_user_will_play()
        InteractiveMinimaxGame.run_game(self.game, user_playing_as=self.user_playing_as,
            eval_fn=self.eval_fn, depth_limit=self.depth_limit)

    @staticmethod
    def try_play(game, eval_fn, depth_limit, play_fn):
        print("\n\n")
        print(game.showBoard())
        play_fn(game, eval_fn, depth_limit)

    @staticmethod
    def run_game(game: Game, user_playing_as: str, eval_fn, depth_limit: int):
        if user_playing_as == "b":
            InteractiveMinimaxGame.try_play(game, eval_fn, depth_limit, InteractiveMinimaxGame.doPlayerPlay)

        curr_play = InteractiveMinimaxGame.doMinimaxPlay

        while game.getWinner() is None:
            InteractiveMinimaxGame.try_play(game, eval_fn, depth_limit, curr_play)
            if user_playing_as != "n":
                if curr_play == InteractiveMinimaxGame.doMinimaxPlay:
                    curr_play = InteractiveMinimaxGame.doPlayerPlay
                else:
                    curr_play = InteractiveMinimaxGame.doMinimaxPlay


        print("\n\n")
        print(game.showBoard())

        final_score = eval_fn(game)

        if final_score == 0:
            print("Draw!")
        elif final_score > 0:
            print("Max wins!")
        else:
            print("Min wins!")

    @staticmethod
    def get_who_user_will_play():
        print("Play as black or white? (n for no player)")
        while True:
            response = input('(b/w/n)> ')
            if response in ["w", "b", "n"]:
                return response
            else:
                print("Enter 'b' or 'w'")

    @staticmethod
    def doPlayerPlay(game: Game, eval, depth_limit) -> None:
        moves = game.getValidMoves()
        if len(moves) == 0:
            return
        print("Possible moves:")
        for i, move in enumerate(moves):
            game.doMove(move)
            val = minimax_val(game, eval, float('-inf'), float('inf'), depth_limit)
            game.undoMoves(1)
            print("  {}) {} ({})".format(i+1, move, val))

        move = ""
        
        while True:
            choice = input('> ')
            try:
                if choice == 'q':
                    exit(0)
                elif choice == 'h':
                    print(game.saveBoardState())
                    continue
                choice = int(choice)
                if choice > 0 and choice <= len(moves):
                    move = moves[choice-1]
                    break
                print("Enter a number between 1 and {}".format(len(moves)))
            except ValueError:
                print("Enter an integer")
        
        game.doMove(move)

    @staticmethod
    def doMinimaxPlay(game: Game, eval, depth_limit) -> None:
        move = minimax_best_move(game, eval, depth_limit=depth_limit)
        print("Minimax plays {}".format(move))
        game.doMove(move)


if __name__ == "__main__":
    game_options = ['Checkers', 'Othello', 'Basic Connect4', 'C4Pop10']
    if TicTacToeGame is not None:
        game_options.append('Tic Tac Toe')

    print("Game options:")
    for i, opt in enumerate(game_options):
        print(f"  {i+1}) {opt}")


    while True:
        response = input('> ')
        if response == '1':
            depth_limit = 6
            game = CheckersGame()
            eval = GameEvalFuncs(eval_checkers_1)
            break
        elif response == '2':
            depth_limit = 4
            game = OthelloGame()
            eval = GameEvalFuncs(eval_othello_1)
            break
        elif response == '3':
            depth_limit = 4
            game = Connect4()
            eval = GameEvalFuncs(eval_connect4_3)
            break
        elif response == '3':
            depth_limit = 6
            game = C4Pop10Game()
            eval = eval_c4pop10_1
            break
        elif TicTacToeGame is not None and response == '5':
            depth_limit = 9
            game = TicTacToeGame()
            eval = eval_tic_tac_toe_1
            break
        print("Choices are " + ', '.join([f"'{i+1}'" for i in range(len(game_options))]))

    InteractiveMinimaxGame(game, eval_fn=eval, depth_limit=depth_limit).play()