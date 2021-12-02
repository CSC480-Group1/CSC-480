from Games import Game
import random
import traceback

has_tqdm = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    has_tqdm = False

depth_limit = 2

def set_depth_limit(limit: int) -> None:
    global depth_limit
    depth_limit = limit

_tt = {}
def _tt_get(key, new_depth: int, depth_limt: int, eval):
    tt_val = _tt.get(key, None)
    if tt_val is None:
        return False

    # print(tt_val)
    score, depth, at_depth_limit = tt_val
    # print('found one')
    # print(score, depth)
    if depth == new_depth:
        return score

    if at_depth_limit:
        return False
    # print('New one')

    raw_score = eval.remove_depth_from_score(score, depth)
    new_depth_score = eval.depth_affected_score(raw_score, new_depth)
    # print(score, depth, new_depth, raw_score, new_depth_score)
    _tt_put(key, new_depth, new_depth_score, depth_limit)

    return new_depth_score

def _tt_put(key, depth: int, score: float, depth_limit: int):
    # if score > 0.14 and score < 0.15:
    #     print(score, depth)
    #     try:
    #         if depth < 6:
    #             raise Exception("Weird depth")
    #     except Exception:
    #         traceback.print_stack()
    _tt[key] = (score, depth, depth_limit <= depth)

def minimax_val(game: Game, eval, alpha: float, beta: float, depthLimit: int, curr_depth=1) -> int:
    key = game.getBoardKey()

    in_right_hist = game.history == [3, 0, 0, 0, 2, 0, 1]
    if in_right_hist:
        print('\n\n ============ AM HERE ============= \n\n')

    if key in _tt:
        if in_right_hist:
            print(key)
            print('YEYE')
            print(_tt[key])
        tt_val = _tt_get(key, curr_depth, depthLimit, eval)
        if tt_val:
            return tt_val
    moves = game.getValidMoves()
    if curr_depth == depthLimit or len(moves) == 0:
        if in_right_hist or key == "[['.', '.', 'W', 'W', 'B', 'W'], ['.', '.', '.', '.', '.', 'B'], ['.', '.', '.', '.', '.', 'B'], ['.', '.', '.', '.', '.', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]":
            print('HEHE')
        score = eval.evaluator(game, curr_depth)
        _tt_put(key, curr_depth, score, depthLimit)
        return score
    
    if game.getWhoseMove() == 'BLACK':
        max_value = float('-inf')
        for move in moves:
            # print(f'\nMOVE {move} at depth {curr_depth} as {game.getWhoseMove()}\n')
            temp_board = game.showBoard()
            game.doMove(move)
            successor_value = minimax_val(game, eval, alpha, beta, depthLimit, curr_depth+1)
            # if move > 5:
            #     print(f'\nMOVE {move} at depth {curr_depth} as {game.getWhoseMove()}\n')
            #     print('Successor value', successor_value)
            #     print('Before')
            #     print(temp_board)
            #     print('After')
            #     game.printBoard()

            game.undoMoves(1)

            max_value = max(max_value, successor_value)
            if successor_value >= beta:
                return successor_value
            alpha = max(alpha, successor_value)

        return max_value
    else:
        min_value = float('inf')
        for move in moves:
            temp_board = game.showBoard()
            game.doMove(move)
            successor_value = minimax_val(game, eval, alpha, beta, depthLimit,curr_depth+1)
            # if move > 5:
            #     print(f'\nMOVE {move} at depth {curr_depth} as {game.getWhoseMove()}\n')
            #     print('Successor value', successor_value)
            #     print('Before')
            #     print(temp_board)
            #     print('After')
            #     game.printBoard()
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
    print('in minimax best move', game.getWhoseMove())

    if has_tqdm:
        moveitr = tqdm(moves, desc="Calculating minimax")
    else:
        moveitr = moves
    for move in moveitr:
        game.doMove(move)
        val = minimax_val(game, eval, float('-inf'), float('inf'), depth_limit)
        print(move, val)
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

    # return random.choice(possibleGoodMoves)
    return possibleGoodMoves[0]
