from Games import *
from eval_funcs import eval_connect4_1

z = Connect4()
# z.doMove(1)

# print(eval_connect4_1(z))

# z.doMove(0)

# print(eval_connect4_1(z))

# for i in range(0, 10):
#     z.doMove(i % 2)
#     x = eval_connect4_1(z)
#     if x > 0:
#         z.showBoard()
#         break
# for i in range(2, 2+4):
#     for j in range(2):
#         z.doMove(i)
#         x = eval_connect4_1(z)
#         if x > 0:
#             z.showBoard()
#             break
# board_moves = [0, 1, 1, 2, 2, 3, 2, 3, 3, 5, 3]
# for i in board_moves:
#     z.doMove(i)
#     x = eval_connect4_1(z)
#     if x > 0:
#         z.showBoard()
#         break
# z.doMove(0) #R
# z.doMove(1) #Y
# z.doMove(1) #R
# z.doMove(2) #Y
# z.doMove(2) #R
# z.doMove(3) #Y
# z.doMove(2) #R
# z.doMove(3) #Y
# z.doMove(3) #R
# z.doMove(4) #Y
# z.doMove(3) #R
#                       W4 B  W  B  W3    W2    W1
board_moves = [3, 3, 3, 3, 4, 4, 5, 4, 0, 5, 0, 6]
for i in board_moves:
    z.doMove(i)
    x = eval_connect4_1(z, 1)
    print(i, x)
    if x > 0:
        z.showBoard()
        break

z.printBoard()
