from Games import *
from eval_funcs import *
from minimax import *

def doPlayerPlay(game: Game, eval) -> None:
    moves = game.getValidMoves()
    if len(moves) == 0:
        return
    print("Possible moves:")
    for i, move in enumerate(moves):
        # print(f'BEFORE MOVE {move}')
        # print(game.showBoard())
        game.doMove(move)
        # print(f'BEFORE MINIMAX {move}')
        # print(game.showBoard())
        val = minimax_val(game, eval, float('-inf'), float('inf'), 2)
        # print(f'AFTER MINIMAX {move}')
        # print(game.showBoard())
        game.undoMoves(1)
        # print(f'AFTER UNDO {move}')
        # print(game.showBoard())
        print("  {}) {} ({})".format(i+1, move, val))

    # print('Game board')
    # print(game.showBoard())
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

def doMinimaxPlay(game: Game, eval) -> None:
    move = minimax_best_move(game, eval)
    print("Minimax plays {}".format(move))
    game.doMove(move)


print("Game options:")
print("  1) Checkers")
print("  2) Othello")
print("  3) Basic Connect4")

while True:
    response = input('> ')
    if response == '1':
        set_depth_limit(6)
        game = CheckersGame()
        eval = GameEvalFuncs(eval_checkers_1)
        break
    elif response == '2':
        set_depth_limit(4)
        game = OthelloGame()
        eval = GameEvalFuncs(eval_othello_1)
        break
    elif response == '3':
        set_depth_limit(10)
        game = Connect4()
        eval = GameEvalFuncs(eval_connect4_1, connect4_get_unaffected_score, connect4_depth_affected_score)
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
    # print('IN HERE')
    moves = game.getValidMoves()
    if len(moves) == 0:
        break
    print("\n\n")
    print(game.showBoard())
    doMinimaxPlay(game, eval)
    # print('HERE!')
    # print(game.showBoard())
    if not no_player:
        print("\n\n")
        print(game.showBoard())
        doPlayerPlay(game, eval)

print("\n\n")
print(game.showBoard())

final_score = eval.evaluator(game, 0)

if final_score == 0:
    print("Draw!")
elif final_score > 0:
    print("Black wins!")
else:
    print("White wins!")
