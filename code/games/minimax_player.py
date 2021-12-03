from Games import *
from eval_funcs import *
from minimax import *


def doPlayerPlay(game: Game, eval) -> None:
    moves = game.getValidMoves()
    if len(moves) == 0:
        return
    print("Possible moves:")
    for i, move in enumerate(moves):
        game.doMove(move)
        val = minimax_val(game, eval, float('-inf'), float('inf'), 9)
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

def doMinimaxPlay(game: Game, eval, depth_limit) -> None:
    move = minimax_best_move(game, eval, depth_limit=depth_limit)
    print("Minimax plays {}".format(move))
    game.doMove(move)

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
        eval = GameEvalFuncs(eval_connect4_1)
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

no_player = False

print("Play as black or white? (n for no player)")
while True:
    response = input('(b/w/n)> ')
    if response == "b":
        print("\n\n")
        print(game.showBoard())
        doPlayerPlay(game, eval)
        break
    elif response == "w":
        break
    elif response == "n":
        no_player = True
        break
    else:
        print("Enter 'b' or 'w'")

while True:
    if game.getWinner() is not None:
        break
    print("\n\n")
    print(game.showBoard())
    doMinimaxPlay(game, eval, depth_limit)
    if not no_player:
        if game.getWinner() is not None:
            break
        print("\n\n")
        print(game.showBoard())
        doPlayerPlay(game, eval)

print("\n\n")
print(game.showBoard())

final_score = eval(game)

if final_score == 0:
    print("Draw!")
elif final_score > 0:
    print("Max wins!")
else:
    print("Min wins!")
