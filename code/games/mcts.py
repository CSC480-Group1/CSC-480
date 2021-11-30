import math
import random
from Games import Game

has_tqdm = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    has_tqdm = False

def _next_player(player):
    if player == 'max':
        return 'min'
    elif player == 'min':
        return 'max'
    else:
        raise ValueError('Unknown player "{}"'.format(player))

class _Game_Lookahead:
    def __init__(self, game: Game, depth = 0):
        self.game = game
        self.depth = depth

    def doMove(self, move: str):
        self.depth += 1
        self.game.doMove(move)
    
    def undoMoves(self, moveCount: int):
        self.depth = max(0, self.depth - moveCount)
        self.game.undoMoves(moveCount)

class _MCTS_Node:
    def __init__(self, move, depth, parent, player):
        self.min_wins = 0
        self.max_wins = 0
        self.count = 0
        self.move = move
        self.parent = parent
        self.children = {}
        self.player = player
        self.depth = depth
    
    def add_child(self, move):
        if move in self.children:
            raise ValueError('Child already exists')
        else:
            self.children[move] = _MCTS_Node(move, self.depth + 1, self, _next_player(self.player))
            return self.children[move]
    
    def _get_p_win(self, player):
        if self.count == 0:
            raise ValueError("Must be updated at least once to get win probability")
        if player == 'min':
            return self.min_wins / self.count
        elif player == 'max':
            return self.max_wins / self.count
        else:
            raise ValueError('Unknown player "{}"'.format(player))
    
    def _get_expected_value(self):
        if self.count == 0:
            raise ValueError("Must be updated at least once to get expected value")
        return (self.max_wins - self.min_wins) / self.count

    def _get_explore_term(self, parent, c=1):
        if parent is not None:
            return c * math.sqrt(2 * math.log(parent.count) / self.count)
        else:
            return 0

    def get_ucb(self, c):
        if self.count == 0:
            raise ValueError("Must be updated at least once to calculate UCB")
        p_win = self._get_expected_value()
        if self.player == "max":
            p_win *= -1
        explore_term = self._get_explore_term(self.parent, c)
        return p_win + explore_term
    
def _expand(game: _Game_Lookahead, node):
    # Make sure the game state is at the current node
    assert game.depth == node.depth
    for move in game.game.getValidMoves():
        child = None
        try:
            child = node.add_child(move)
        except ValueError:
            continue
        return child
    
    return None


def _best_child(node, c):
    return max(node.children.values(), key=lambda child: child.get_ucb(c))


def _tree_policy(game: _Game_Lookahead, node, c):
    assert game.depth == node.depth

    if game.game.getWinner() is not None:
        return node
    
    unexplored_child = _expand(game, node)
    if unexplored_child is not None:
        game.doMove(unexplored_child.move)
        return unexplored_child
    else:
        next = _best_child(node, c)
        game.doMove(next.move)
        return _tree_policy(game, next, c)

def _backup(node, winner):
    if node is None:
        return
    node.count += 1
    if winner == 'min':
        node.min_wins += 1
    elif winner == 'max':
        node.max_wins += 1
    _backup(node.parent, winner)

def _default_policy(game: _Game_Lookahead):
    winner = game.game.getWinner()
    while winner is None:
        game.doMove(random.choice(game.game.getValidMoves()))
        winner = game.game.getWinner()
    return winner

def mcts(game: Game, player: str, iterations: int, quiet=False, c=1):
    key = game.getBoardKey()
    start_node = _MCTS_Node(None, 0, None, player)
    lookahead = _Game_Lookahead(game)
    iter = range(iterations)
    if not quiet and has_tqdm:
        iter = tqdm(iter, desc='Calculating Monte-Carlo')
    for _ in iter:
        node = _tree_policy(lookahead, start_node, c)
        value = _default_policy(lookahead)
        lookahead.undoMoves(lookahead.depth)
        _backup(node, value)
        assert key == game.getBoardKey()
    action = _best_child(start_node, 0).move
    return action