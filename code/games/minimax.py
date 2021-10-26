from Games import Game
import random

has_tqdm = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    has_tqdm = False

depth_limit = 2

def set_depth_limit(limit: int) -> None:
    global depth_limit
    depth_limit = limit

def minimax_val(game: Game, eval, alpha: float, beta: float, depthLimit: int) -> int:
    moves = game.getValidMoves()
    if depthLimit == 0 or len(moves) == 0:
        return eval(game)
    
    if game.getWhoseMove() == 'BLACK':
        max_value = float('-inf')
        for move in moves:
            game.doMove(move)
            successor_value = minimax_val(game, eval, alpha, beta, depthLimit-1)
            game.undoMoves(1)

            max_value = max(max_value, successor_value)
            if successor_value >= beta:
                return successor_value
            alpha = max(alpha, successor_value)

        return max_value
    else:
        min_value = float('inf')
        for move in moves:
            game.doMove(move)
            successor_value = minimax_val(game, eval, alpha, beta, depthLimit-1)
            game.undoMoves(1)

            min_value = min(min_value, successor_value)
            if successor_value <= alpha:
                return successor_value
            beta = min(beta, successor_value)
        
        return min_value

def minimax_best_move(game: Game, eval) -> str:
    global depth_limit
    moves = game.getValidMoves()
    if len(moves) == 0:
        raise ValueError('Game is already over')
    
    vals = {}

    if has_tqdm:
        moveitr = tqdm(moves, desc="Calculating minimax")
    else:
        moveitr = moves
    for move in moveitr:
        game.doMove(move)
        val = minimax_val(game, eval, float('-inf'), float('inf'), depth_limit)
        game.undoMoves(1)
        vals[move] = val

    # print(vals)
    
    if game.getWhoseMove() == 'BLACK':
        best = max(vals.values())
    else:
        best = min(vals.values())

    # print(best)
    
    possibleGoodMoves = []
    for move in moves:
        if vals[move] == best:
            possibleGoodMoves.append(move)
    
    assert len(possibleGoodMoves) != 0

    return random.choice(possibleGoodMoves)
