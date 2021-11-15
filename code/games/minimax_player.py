from Games import *
from eval_funcs import *
from minimax import *

tt = {}

def doPlayerPlay(game: Game, eval) -> None:
    moves = game.getValidMoves()
    print("Possible moves:")
    for i, move in enumerate(moves):
        game.doMove(move)
        val = minimax_val(game, eval, float('-inf'), float('inf'), 6, tt=tt)
        game.undoMoves(1)
        print("  {}) {} ({})".format(i+1, move, val))

    move = ""
    
    while True:
        choice = input('> ')
        try:
            if choice == 'q':
                exit(0)
            choice = int(choice)
            if choice > 0 and choice <= len(moves):
                move = moves[choice-1]
                break
            print("Enter a number between 1 and {}".format(len(moves)))
        except ValueError:
            print("Enter an integer")
    
    game.doMove(move)

def doMinimaxPlay(game: Game, eval) -> None:
    move = minimax_best_move(game, eval, tt=tt)
    print("Minimax plays {}".format(move))
    game.doMove(move)


print("Game options:")
print("  1) Checkers")
print("  2) Othello")
print("  3) C4Pop10")

while True:
    response = input('> ')
    if response == '1':
        set_depth_limit(6)
        game = CheckersGame()
        eval = eval_checkers_1
        break
    elif response == '2':
        set_depth_limit(4)
        game = OthelloGame()
        eval = eval_othello_1
        break
    elif response == '3':
        set_depth_limit(6)
        game = C4Pop10Game()
        eval = eval_c4pop10_1
        break
    print("Choices are '1' or '2'")

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
    moves = game.getValidMoves()
    if len(moves) == 0:
        break
    print("\n\n")
    print(game.showBoard())
    doMinimaxPlay(game, eval)
    if not no_player:
        print("\n\n")
        print(game.showBoard())
        doPlayerPlay(game, eval)

print("\n\n")
print(game.showBoard())

final_score = eval(game)

if final_score == 0:
    print("Draw!")
elif final_score > 0:
    print("Black wins!")
else:
    print("White wins!")
