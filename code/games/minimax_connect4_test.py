from Games import *
from eval_funcs import *
from minimax import *

z = Connect4()
# z.loadBoardState([0, 1, 2, 5, 3, 1, 4, 4, 2, 3, 2, 5, 3, 3, 3, 4, 1, 2])
# 4 1 3 2
z.loadBoardState([3, 0, 0, 0, 2, 0, 1])
set_depth_limit(6)
print(minimax_best_move(z, GameEvalFuncs(eval_connect4_1, connect4_get_unaffected_score, connect4_depth_affected_score)))
# board_to_load = """
# .  .  .  .  .  .  .
# .  .  .  B  .  .  .
# .  .  W  W  .  .  .
# .  B  B  B  W  .  .
# .  W  B  W  W  W  .
# B  W  B  B  B  W  .
# """

# board_arr = [(['.'] * (z.getDimensions()[1])) for _ in range(z.getDimensions()[0])]
# board_vals_not_none = 0
# for i, val in enumerate(board_to_load.strip().split('\n')):
#     for j, val2 in enumerate(val.replace(' ', '')):
#         board_arr[i][j] = val2
#         if val is not NONE:
#             board_vals_not_none += 1

# print(board_arr)

# z.loadBoard(board_arr, board_vals_not_none)
# z.printBoard()
# print(z.getWhoseMove())
# set_depth_limit(2)
""" for m in z.getValidMoves():
    z.doMove(m)
    z.printBoard()
    print(m, eval_connect4_1(z, 0))
    z.undoMoves(1) """