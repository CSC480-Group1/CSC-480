# Implementing the Minimax Algorithm with Connect X

### Connect X Implementation

For this, we will assume we have a basic working Connect X implementation, which can have a variable number rows/columns and win condition. If you want to see the implementation, check the `Show all code` checkbox at the top.


```python
from itertools import groupby, chain
```


```python
NONE = '.'
BLACK = 'B'
WHITE = 'W'
BLACK_PLAYER = 'BLACK'
WHITE_PLAYER = 'WHITE'

def diagonalsPos(matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

def diagonalsNeg(matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]


class Connect4:
    def __init__(self, cols=7, rows=6, requiredToWin=4):
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        self.turn = BLACK
        self.board = [[NONE] * rows for _ in range(cols)]
        self.game_over = False
        self.move_history = []

    def reset_game(self):
        self.turn = BLACK
        self.board = [[NONE] * self.rows for _ in range(self.cols)]
        self.game_over = False
        self.move_history = []

    def insert(self, column, shadow=False):
        color = self.turn
        c = self.board[column]
        if c[0] != NONE:
            if not shadow:
                self.printBoard()
                print(f'Column {column} is full')
            return False

        i = -1
        while c[i] != NONE:
            i -= 1

        if not shadow:
            c[i] = color
            self.move_history.append(column)

            have_won = self.checkForWin()
            if have_won:
                self.game_over = True
            self.turn = WHITE if self.turn == BLACK else BLACK
        return True

    def getWhoseMove(self):
        return BLACK_PLAYER if self.turn == BLACK else WHITE_PLAYER

    def checkForWin(self):
        w = self.getWinner()
        return w

    def getWinningPlayer(self):
        w = self.checkForWin()
        if w is not NONE:
            return BLACK_PLAYER if w == BLACK else WHITE_PLAYER
        
        return None

    def getWinner(self):
        lines = (
            self.board,  # columns
            zip(*self.board),  # rows
            diagonalsPos(self.board, self.cols, self.rows),  # positive diagonals
            diagonalsNeg(self.board, self.cols, self.rows)  # negative diagonals
        )
        
        print(str(self.board))

        for line in chain(*lines):
            for color, group in groupby(line):
                if str(self.board) == "[['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', '.', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]":
                    print(color, group, list(group))
                if color != NONE and len(list(group)) >= self.win:
                    return color

    @staticmethod
    def getRepr(board, rows, cols):
        string = '   ' + '  '.join(map(str, range(cols))) + '\n'
        for y in range(rows):
            string += '  '.join([str(y)] + [str(board[x][y]) for x in range(cols)]) + '\n'

        return string

    @staticmethod
    def get_game_from_history(history, *args, **game_params):
        g = Connect4(*args, **game_params)
        for move in history:
            g.insert(move)
        
        return g

    def undoLastMove(self):
        if len(self.move_history) == 0:
            return
        
        move_removed = self.move_history.pop()
        c = self.board[move_removed]
        i = -1
        while c[i] != NONE and abs(i) < self.rows:
            i -= 1

        if c[i] == NONE:
            turn_found = c[i + 1]
            c[i + 1] = NONE
        else:
            turn_found = c[i]
            c[i] = NONE            

        self.turn = turn_found
        self.game_over = False

    def getBoardRepr(self):
        return Connect4.getRepr(self.board, self.rows, self.cols)

    def printBoard(self):
        print(self.getBoardRepr())

    def getValidMoves(self):
        if self.game_over:
            return []

        valid_moves = list(filter(lambda col: self.insert(col, shadow=True), range(self.cols)))
        for c in range(self.cols):
            success = self.insert(c, shadow=True)
        
        return valid_moves
```

## Playing the game.

### Starting a game

A game is initialized by creating a new `Connect4` object. The constructor signature `def __init__(self, cols=7, rows=6, requiredToWin=4)` tells us that if we don't provide any other options, are game will default to using 7 columns, 6 rows, and a win condition of 4 in a row. We can override each of these options as we please.

### Playing the game

In its current state, this is a manual 2 player game. The colors for each player are black and white. Let's talk about what we can do while playing:
- `getWhoseMove()` -- returns whose move it is (black/white)
- `getValidMoves()` -- returns list of valid columns a player can make their move on (0-indexed)
- `insert(column)` -- plays the `column` as the current player's move
- `printBoard()` -- prints the current board 
- `checkForWin()` -- returns who won, if someone has
- `undoLastMove()` -- undoes the last move

## Let's play a basic game!

Just to test our game, we'll use the default parameters and the following moveset:
```python
Black:
[0, 1, 2, 3]
White:
[0, 1, 2]
```

This should result in a win for black.

## Now to run out first test!


```python
game = Connect4()
black_moves = [0, 1, 2, 3]
white_moves = [0, 1, 2]

print('Winner at start:', game.checkForWin())
print('Game board at start:')
game.printBoard()

for i in range((len(black_moves) + len(white_moves))):
    if game.getWhoseMove() == BLACK_PLAYER:
        next_move = black_moves.pop(0)
    else:
        next_move = white_moves.pop(0)

    game.insert(next_move)

print('Game board after all moves:')
game.printBoard()
print('Winner:', game.checkForWin())
```

    Winner at start: None
    Game board at start:
       0  1  2  3  4  5  6
    0  .  .  .  .  .  .  .
    1  .  .  .  .  .  .  .
    2  .  .  .  .  .  .  .
    3  .  .  .  .  .  .  .
    4  .  .  .  .  .  .  .
    5  .  .  .  .  .  .  .
    
    Game board after all moves:
       0  1  2  3  4  5  6
    0  .  .  .  .  .  .  .
    1  .  .  .  .  .  .  .
    2  .  .  .  .  .  .  .
    3  .  .  .  .  .  .  .
    4  W  W  W  .  .  .  .
    5  B  B  B  B  .  .  .
    
    Winner: B


## Playing against an Agent

Now let's say we want to play against some automated agent. Well, we probably want something competitive (good at the game). We can make a competitive agent using the [Minimax algorithm](https://en.wikipedia.org/wiki/Minimax).

The idea of a basic minimax is that we have 2 players: min and max. Each assumes the other player will play optimally. 

Here are the basic steps for the algorithm:
- Find all available moves for the player (min or max)
- If there are no moves:
  - Return the board state as a "score" -- we call this our **utility** function
- For each possible move:
  - Do that move
  - Call minimax on the new board state
  - If the score returned is better than any previous score:
    - New best score is that one
- Return best score

### Some complexities
This is the general outline of the algorithm. One thing that still needs to be implemented is how being min vs max differs for a score. This is important, since if our player is black and minimax returns say `1.0` as a win for black and `1.0` as a win for white, both seem like valid moves. However, we want to make the move that returns to us a win for black here.

To do this, let's make some assumptions: a larger score is better for max and a smaller score is better for min.

Then we can say `-1.0` may be a win for white and `1.0` would be a win for black in the case mentioned above.

So let's change our algorithm a bit now. After the **Do that move** step:
- Call minimax on new board state.
- If player is max and the returned score is **larger** than any other we've seen before, our new best move is the one we made above.
- If player is min and the returned score is **smaller** than any other we've seen before, our new best move is the one we made above.

## Visualizing the algorithm

Let's imagine making each move as building a tree, where each move gets an assigned score.

Let's imagine we have the following board state and are playing Connect 3 instead:
```
   0  1  2
0  .  W  .
1  .  B  .
2  W  W  B
3  B  W  B
```

We can see the current turn is `blacks`'s, so we want a high score. Black can either make a move in column 0 or column 2. Each indentation is a new tree level. Let's examine column 0 as a move first:

`Black plays 0`:
   - Game now done? -> No
   - White can either play 0 or 2
   - `White plays 0`
      - Game now done? -> No
      - Black can only play 2
      - `Black plays 2`
         - Game now done? -> Yes -> Score: 1.0 (black wins)
      - Final score for if `white plays 0` = min(1.0) = 1.0 (black wins)
   - `White plays 2`
      - Game now done? -> No
      - Black can play either 0 or 2
      - `Black plays 0`
         - Game now done? -> Yes -> Score: 1.0 (black wins)
      - `Black plays 2`
         - Game now done? -> No
         - White can only play 0
         - `White plays 0`
            - Game now done? -> Yes -> Score: 0.0 (Draw)
         - Final score for if `black plays 2` = max(0.0, 1.0) = 1.0 (black wins)
      - Final score for if `white plays 2` = min(1.0, 1.0) = 1.0 (black wins)
   - Final score for if `black plays 0` = min(1.0, 1.0) (black wins)

We can see in either case, the best score is 1.0, or a win for black. So white playing 0 is a score of 1.0 from minimax.

<qinline>

<question>

Now try to do black's other move on your own:

`Black plays 2`:

</question>

<answer>

- Game now done? -> Yes -> Score: 1.0 (black wins)

</answer>

</qinline>


Alright, now that that's out of the way, let's talk about some of the key takeways. First, we can see **_if black plays optimally they will win_**. This is because white must block in column 2 first. Then, black can also place in column 2 to force white to play in column 0, which ultimately lets black play in column 0 again and give it 3 in a row on the negative diagonal.

We can represent this move sequence as: `[2, 2, 0, 0]`.

## Now let's prove this using minimax 



```python
def minimax_best_move(game: Connect4):
    current_player = game.getWhoseMove()
    valid_moves = game.getValidMoves()
    if len(valid_moves) == 0:
        raise Exception('Cannot make a move')

    best_move, best_score = None, None
    for move in valid_moves:
        game.insert(move)
        minimax_score = minimax(game)
        game.undoLastMove()
        if best_move is None:
            best_move = move
            best_score = minimax_score
        elif current_player == BLACK_PLAYER and best_score < minimax_score:
            best_score = minimax_score
            best_move = move
        elif current_player == WHITE_PLAYER and best_score > minimax_score:
            best_score = minimax_score
            best_move = move
    
    return best_move

def minimax(game: Connect4):
    current_player = game.getWhoseMove()
    valid_moves = game.getValidMoves()
    if len(valid_moves) == 0:
        return connect4_utility(game)

    best_score = float('-inf') if current_player == BLACK_PLAYER else float('inf')
    for successive_move in valid_moves:
        game.insert(successive_move)
        move_score = minimax(game)
        game.undoLastMove()
        if current_player == BLACK_PLAYER:
            best_score = max(best_score, move_score)
        else:
            best_score = min(best_score, move_score)

    return best_score

def connect4_utility(game: Connect4):
    winner = game.checkForWin()
    if winner == BLACK:
        return 1.0
    elif winner == WHITE:
        return -1.0
    else:
        return 0
```

### Let's setup for running our tests!


```python
def run_minimax_game(move_history, requiredToWin=3, cols=3, rows=4):
    game = Connect4.get_game_from_history(move_history, requiredToWin=requiredToWin, cols=cols, rows=rows)
    game.printBoard()

    # Let's test minimax
    runs = 0
    while len(game.getValidMoves()) > 0:
        player = game.getWhoseMove()
        best_move = minimax_best_move(game)
        game.insert(best_move)
        print(player, 'played', best_move)
        runs += 1
        if runs > 4:
            raise Exception('Too many runs')

    game.printBoard()
    print('Winner:', game.getWinningPlayer())
```


```python
run_minimax_game([0, 1, 2, 0, 2, 1, 1, 1])
```

       0  1  2
    0  .  W  .
    1  .  B  .
    2  W  W  B
    3  B  W  B
    
    BLACK played 0
    WHITE played 0
    BLACK played 2
       0  1  2
    0  W  W  .
    1  B  B  B
    2  W  W  B
    3  B  W  B
    
    Winner: BLACK


## Choosing Optimally

<qinline>

<question>

### Answer this before reading on!

Ok, in the above we see that black made the right moves to win. But why didn't it just choose column 2 to begin with a win?

</question>

<answer>

The reason why is because we aren't picking the choice that leads to the fastest best game outcome, just to the one that leads to a best outcome in general. There can be different ways to do that as we see above. Black can play either 0 or 2 as a move and still win if it plays optimally afterwards. For that reason, the choice black makes is arbitrary.

So what if we want to choose the best game outcome optimally (least number of moves)?

</answer>

</qinline>

## Factoring in Depth

We can include a depth factor in our score that describes how many steps it took to make it there. A solution with more steps gets a worse score.

This not only leads to an optimal solution for winning but also can be used to delay a loss for as long as possible.

### Implementing Depth

To do this, we simply just need to keep track of how many moves we have made from the start of minimax. This tells us how many moves in minimax is from the original move we are testing.




```python
def minimax(game: Connect4, depth=0):
    current_player = game.getWhoseMove()
    valid_moves = game.getValidMoves()
    if len(valid_moves) == 0:
        return connect4_utility_with_depth(game, depth)

    best_score = float('-inf') if current_player == BLACK_PLAYER else float('inf')
    for successive_move in valid_moves:
        game.insert(successive_move)
        move_score = minimax(game, depth + 1)
        game.undoLastMove()
        if current_player == BLACK_PLAYER:
            best_score = max(best_score, move_score)
        else:
            best_score = min(best_score, move_score)

    return best_score

def connect4_utility_with_depth(game: Connect4, depth: int):
    return connect4_utility(game) * (1 / (1 + depth))
```


```python
run_minimax_game([0, 1, 2, 0, 2, 1, 1, 1])
```

       0  1  2
    0  .  W  .
    1  .  B  .
    2  W  W  B
    3  B  W  B
    
    BLACK played 2
       0  1  2
    0  .  W  .
    1  .  B  B
    2  W  W  B
    3  B  W  B
    
    Winner: BLACK


## Proving we can Delay
Let's imagine we have this board state:
```
   0 1 2
0  . . .
1  W B .
2  B W B
```

In any case here, white will lose. Let's see each case:

- White plays 0 to block diagonal
   - Black plays 1
   - White plays 2 since only column left
   - Blacks plays 2 and wins
- White plays 1
   - Black plays 0 and wins on diagonal
- White plays 2
   - Black plays 0 and wins on diagonal

Any move that white plays results in a win for black. However, white can hope black makes a mistake. If black were to play 2 instead of 1 after white played 0, then we could draw instead. Thus white should play 0 as a hope.


```python
# Testing long delay
run_minimax_game([0, 1, 2, 0, 1], rows=3, cols=3)
```

       0  1  2
    0  .  .  .
    1  W  B  .
    2  B  W  B
    
    WHITE played 0
    BLACK played 1
    WHITE played 2
    BLACK played 2
       0  1  2
    0  W  B  B
    1  W  B  W
    2  B  W  B
    
    Winner: BLACK


But maybe it just played 0 because it was the first move it came across...


```python
# Testing long delay
run_minimax_game([0, 1, 2, 2, 1], rows=3, cols=3)
```

       0  1  2
    0  .  .  .
    1  .  B  W
    2  B  W  B
    
    WHITE played 2
    BLACK played 1
    WHITE played 0
    BLACK played 0
       0  1  2
    0  B  B  W
    1  W  B  W
    2  B  W  B
    
    Winner: BLACK


In either case here, we see that even if the agent expects to lose, it will try to play for as long as possible.


```python
game = Connect4()
black_moves = [0, 1, 2, 3]
white_moves = [0, 1, 2]

print('Winner at start:', game.checkForWin())
print('Game board at start:')
game.printBoard()

for i in range((len(black_moves) + len(white_moves))):
    if game.getWhoseMove() == BLACK_PLAYER:
        next_move = black_moves.pop(0)
    else:
        next_move = white_moves.pop(0)

    game.insert(next_move)

print('Game board after all moves:')
game.printBoard()
print('Winner:', game.checkForWin())
```

    [['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    Winner at start: None
    Game board at start:
       0  1  2  3  4  5  6
    0  .  .  .  .  .  .  .
    1  .  .  .  .  .  .  .
    2  .  .  .  .  .  .  .
    3  .  .  .  .  .  .  .
    4  .  .  .  .  .  .  .
    5  .  .  .  .  .  .  .
    
    [['.', '.', '.', '.', '.', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    [['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    [['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', '.', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    [['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    [['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', '.', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    [['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    [['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', '.', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    . <itertools._grouper object at 0x000001E53A2A9F28> ['.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2A9D30> ['W']
    B <itertools._grouper object at 0x000001E53A2A9358> ['B']
    . <itertools._grouper object at 0x000001E53A2A9B70> ['.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2A9358> ['W']
    B <itertools._grouper object at 0x000001E53A2A99B0> ['B']
    . <itertools._grouper object at 0x000001E53A2A9198> ['.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2A99B0> ['W']
    B <itertools._grouper object at 0x000001E53A2A9780> ['B']
    . <itertools._grouper object at 0x000001E53A2A9BE0> ['.', '.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2A9780> ['B']
    . <itertools._grouper object at 0x000001E53A2A9080> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2A94E0> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2A9208> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2A94E0> ['.', '.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2A9080> ['.', '.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2A9A90> ['.', '.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2A9208> ['.', '.', '.', '.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2A94E0> ['W', 'W', 'W']
    . <itertools._grouper object at 0x000001E53A2A9208> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2A9080> ['B', 'B', 'B', 'B']
    . <itertools._grouper object at 0x000001E53A2A9208> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2A9A90> ['.']
    . <itertools._grouper object at 0x000001E53A2A9780> ['.', '.']
    . <itertools._grouper object at 0x000001E53A2A9A90> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2A94E0> ['.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2A9080> ['W']
    . <itertools._grouper object at 0x000001E53A2A9780> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2A9C18> ['B']
    W <itertools._grouper object at 0x000001E53A2A9A90> ['W']
    . <itertools._grouper object at 0x000001E53A2A9748> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2A93C8> ['B']
    W <itertools._grouper object at 0x000001E53A2A9080> ['W']
    . <itertools._grouper object at 0x000001E53A2BAD68> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2BA438> ['B']
    . <itertools._grouper object at 0x000001E53A2A9E80> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2BA438> ['B']
    . <itertools._grouper object at 0x000001E53A2A9080> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BAD68> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2A9A90> ['.', '.']
    . <itertools._grouper object at 0x000001E53A2BAD68> ['.']
    . <itertools._grouper object at 0x000001E53A2BA3C8> ['.']
    . <itertools._grouper object at 0x000001E53A2BA710> ['.', '.']
    . <itertools._grouper object at 0x000001E53A2BA3C8> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA438> ['.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA3C8> ['.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA710> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA3C8> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA438> ['.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA3C8> ['.', '.']
    W <itertools._grouper object at 0x000001E53A2BA710> ['W']
    B <itertools._grouper object at 0x000001E53A2BA438> ['B']
    . <itertools._grouper object at 0x000001E53A2BA400> ['.']
    W <itertools._grouper object at 0x000001E53A2BA438> ['W']
    B <itertools._grouper object at 0x000001E53A2BA390> ['B']
    W <itertools._grouper object at 0x000001E53A2BA0F0> ['W']
    B <itertools._grouper object at 0x000001E53A2BA0B8> ['B']
    B <itertools._grouper object at 0x000001E53A2BA668> ['B']
    Game board after all moves:
       0  1  2  3  4  5  6
    0  .  .  .  .  .  .  .
    1  .  .  .  .  .  .  .
    2  .  .  .  .  .  .  .
    3  .  .  .  .  .  .  .
    4  W  W  W  .  .  .  .
    5  B  B  B  B  .  .  .
    
    [['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', 'W', 'B'], ['.', '.', '.', '.', '.', 'B'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.']]
    . <itertools._grouper object at 0x000001E53A2BADA0> ['.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2BA9E8> ['W']
    B <itertools._grouper object at 0x000001E53A2BA9B0> ['B']
    . <itertools._grouper object at 0x000001E53A2BADD8> ['.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2BA9B0> ['W']
    B <itertools._grouper object at 0x000001E53A2BA5F8> ['B']
    . <itertools._grouper object at 0x000001E53A2BA470> ['.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2BA5F8> ['W']
    B <itertools._grouper object at 0x000001E53A2BA320> ['B']
    . <itertools._grouper object at 0x000001E53A2BA5C0> ['.', '.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2BA320> ['B']
    . <itertools._grouper object at 0x000001E53A2BA748> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA6D8> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA6A0> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA6D8> ['.', '.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA748> ['.', '.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA358> ['.', '.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA6A0> ['.', '.', '.', '.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2BA6D8> ['W', 'W', 'W']
    . <itertools._grouper object at 0x000001E53A2BA6A0> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2BA748> ['B', 'B', 'B', 'B']
    . <itertools._grouper object at 0x000001E53A2BA6A0> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA358> ['.']
    . <itertools._grouper object at 0x000001E53A2BA320> ['.', '.']
    . <itertools._grouper object at 0x000001E53A2BA358> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA6D8> ['.', '.', '.', '.']
    W <itertools._grouper object at 0x000001E53A2BA748> ['W']
    . <itertools._grouper object at 0x000001E53A2BA320> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2BA4A8> ['B']
    W <itertools._grouper object at 0x000001E53A2BA358> ['W']
    . <itertools._grouper object at 0x000001E53A2BA048> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2BA208> ['B']
    W <itertools._grouper object at 0x000001E53A2BA748> ['W']
    . <itertools._grouper object at 0x000001E53A2BA128> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2BA780> ['B']
    . <itertools._grouper object at 0x000001E53A2BA358> ['.', '.', '.', '.']
    B <itertools._grouper object at 0x000001E53A2BA240> ['B']
    . <itertools._grouper object at 0x000001E53A2BA748> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BAC88> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA780> ['.', '.']
    . <itertools._grouper object at 0x000001E53A2BAC88> ['.']
    . <itertools._grouper object at 0x000001E53A2BAF98> ['.']
    . <itertools._grouper object at 0x000001E53A2BA080> ['.', '.']
    . <itertools._grouper object at 0x000001E53A2BAF98> ['.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA240> ['.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA748> ['.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA080> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BAF98> ['.', '.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA240> ['.', '.', '.', '.', '.']
    . <itertools._grouper object at 0x000001E53A2BA748> ['.', '.']
    W <itertools._grouper object at 0x000001E53A2BA080> ['W']
    B <itertools._grouper object at 0x000001E53A2BA240> ['B']
    . <itertools._grouper object at 0x000001E53A2BA828> ['.']
    W <itertools._grouper object at 0x000001E53A2BAF98> ['W']
    B <itertools._grouper object at 0x000001E53A2BA518> ['B']
    W <itertools._grouper object at 0x000001E53A2BA198> ['W']
    B <itertools._grouper object at 0x000001E53A2BA7B8> ['B']
    B <itertools._grouper object at 0x000001E53A2BA588> ['B']
    Winner: None

