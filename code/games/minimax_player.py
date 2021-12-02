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


print("Game options:")
print("  1) Checkers")
print("  2) Othello")
print("  3) Basic Connect4")
print("  4) C4Pop10")
if TicTacToeGame is not None:
    print("  5) Tic Tac Toe")

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
        set_depth_limit(10)
        game = Connect4()
        eval = GameEvalFuncs(eval_connect4_1)
        break
    elif response == '3':
        depth_limit = 6
        game = C4Pop10Game()
        eval = eval_c4pop10_1
        break
    elif TicTacToeGame is not None and response == '4':
        depth_limit = 9
        game = TicTacToeGame()
        eval = eval_tic_tac_toe_1
        break
    if TicTacToeGame is None:
        print("Choices are '1', '2', '3'")
    else:
        print("Choices are '1', '2', '3', '4'")

no_player = False

print("Play as black or white? (n for no player)")
while True:
    response = input('(b/w/n)> ')
    if response == "b":
        print("\n\n")
        print(game.showBoard())
        doPlayerPlay(game, eval)
        # print(game.showBoard())
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
