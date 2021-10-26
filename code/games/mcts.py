from Games import CGame
from BoardTest import getBoardValue
import math
import random

has_tqdm = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    has_tqdm = False

uct_c = math.sqrt(2)

class _MCTS_Node:
    def __init__(self, parent, move: str, game: CGame):
        self.move = move
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = []
        self.unexplored_children = game.getValidMoves()
        self.is_terminal_state = len(self.unexplored_children) == 0
        
        self.player = game.getPlayer()

    def calculate_uct_value(self, parent):
        win_ratio = self.score / self.visits
        return win_ratio + uct_c * math.sqrt(math.log(parent.visits) / self.visits)
    
    def choose_uct_best(self):
        assert len(self.unexplored_children) == 0
        assert len(self.children) != 0
        return max(self.children, key=lambda node: node.calculate_uct_value(self))
    
    def choose_random_unexplored_child(self):
        move = random.choice(self.unexplored_children)
        self.unexplored_children.remove(move)
        return move
        
    def backpropagate(self, delta):
        self.visits += 1
        if self.player == 'max':
            self.score += delta
        elif self.player == 'min':
            self.score -= delta
        else:
            raise Exception('Unexpected player value')
        if self.parent is not None:
            self.parent.backpropagate(delta)

def _evaluate_terminal_state(game: CGame, player: str) -> int:
    boardValue = getBoardValue()

    if boardValue > 0:
        boardValue = 1
    elif boardValue < 0:
        boardValue = -1
    else:
        boardValue = 0
    return boardValue

def _simulate_rollout(game: CGame, player: str) -> int :
    count = 0
    startkey = game.getBoardKey()
    while True:
        moves = game.getValidMoves()
        if len(moves) == 0:
            break
        count += 1
        game.doMove(random.choice(moves))
    
    delta = _evaluate_terminal_state(game, player)
    game.undoMoves(count)
    assert game.getBoardKey() == startkey
    return delta

def mcts(game: CGame, player: str):
    moves = game.getValidMoves()
    assert len(moves) > 0
    if len(moves) == 1:
        return moves[0]
    root = _MCTS_Node(None, "", game)

    iter = range(200)
    if has_tqdm:
        iter = tqdm(iter, desc='Calculating Monte-Carlo')

    startkey = game.getBoardKey()
    
    for _ in iter:
        curr = root
        depth = 0
        while len(curr.unexplored_children) == 0 and not curr.is_terminal_state:
            next = curr.choose_uct_best()
            game.doMove(next.move)
            depth += 1
            curr = next
        if curr.is_terminal_state:
            delta = _evaluate_terminal_state(game, player)
        else:
            move = curr.choose_random_unexplored_child()
            game.doMove(move)
            depth += 1
            delta = _simulate_rollout(game, player)
            curr = _MCTS_Node(curr, move, game)
            curr.parent.children.append(curr)
        curr.backpropagate(delta)
        game.undoMoves(depth)
        assert game.getBoardKey() == startkey
    
    best = root.choose_uct_best()
    return best.move
