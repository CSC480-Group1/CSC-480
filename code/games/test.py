from ai_battle import *
from eval_funcs import *

connect4Game = Connect4()

AIBattle(
    connect4Game,
    MinimaxPlayer(eval_connect4_3, depth_limit=4),
    RandomPlayer()
).go()