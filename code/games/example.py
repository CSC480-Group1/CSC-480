from Games import *
import random
import time

"""

Example of usage of `Game`s.

"""

print("Options:")
print("1. Othello")
print("2. Checkers")
print("3. Connect 4 Pop 10")

option = int(input("> "))

if option == 1:
    game = OthelloGame()
elif option == 2:
    game = CheckersGame()
elif option == 3:
    game = C4Pop10Game()
else:
    print("Invalid option")
    exit(1)

def playGame(game):
    game.undoMoves(100000)
    while True:
        print(game.showBoard())
        moves = game.getValidMoves()
        if len(moves) == 0:
            break
        move = random.choice(moves)
        print(game.getWhoseMove(),"plays", move)
        game.doMove(move)
        time.sleep(0.2)
    print("Done!")

while True:
    playGame(game)

    print("Play again?")
    again = input("(y/n)> ")

    if again != 'y':
        break


