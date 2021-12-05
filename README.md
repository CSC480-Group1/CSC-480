# MCTS and Minimax in Simple Board Games
## A CSC 480 - Artificial Intelligence Project
- CSC 480 Section 1 with Professor Rodrigo Canaan
- Project by Group 1:
   - Jordan Powers
   - Mukhammadorif Sultanov
   - Nicholas Sheffler
   - Benjamin Glossner
- All extenral resources used are listed in _References_ at the end 

<hr>

## Running files
### Setup
On Cal Poly Unix servers:
   1. `ssh \<username\>@unix<1-5>.csc.calpoly.edu`
      - If you are off campus, you need to first connect to the VPN through GlobalProtect. Info can be found [here](https://calpoly.atlassian.net/wiki/spaces/CPKB/pages/2425047/Set+up+VPN)
   1. `git clone https://github.com/CSC480-Group1/CSC-480.git`
   1. **OPTIONAL**: make a python virtual environment at this point and activate it
   1. `cd ~/CSC-480`
   1. `python3 -m pip install -r requirements.txt`
      - Or `python3 -m pip install numpy tqdm`
   1. `cd code/games`

<hr>

## Playing against Minimiax/MCTS or watching them battle
- This option is what you want if you want to play against minimax or MCTS in a game of your choice **OR** if you want to watch the agent battle itself
- Navigate to the `code/games` directory

### Selecting a game
- You may be prompted to select a game. In this case, just select the number related to the game you want to play. This will all be prompted for you. This will look like:
```
Game options:
  1) Checkers
  2) Othello
  3) Connect4
  4) C4Pop10
  5) Tic Tac Toe
>
```
> You'd enter `2` to play Othello or `5` for Tic Tac Toe 

### Selecting who you want to play as
- You will be prompted who you want to play as. This will look like:
```
Play as black or white? (n for no player)
(b/w/n)> 
``` 
> Enter `b` for playing as black and making the 1st move, `w` for playing white and making the 2nd move, and `n` for having 2 agents play each other (you don't participate)

### Minimax Option
1. `python3 minimax_player.py`
   - Basic configurations (uses all defaults)
   - Select game by following prompt
   - Select who you want to play as
   - Follow prompts for making moves and good luck!
2. `python3 minimax_player.py --help`
   - Print help/usage message for seeing optional command line arguments
3. `python3 minimax_player.py [--game <game>] [--depth-limit depth] [--eval-fn fn]`
   - This runs a game with minimax with special options (changing parameters... can override the defaults).
   - Each flag/value is optional here. If you don't specify the game, it will prompt you later during the program execution
   - Set the game through the command line by doing `--game <game>`
      - `python3 minimax_player.py --game connect4` will play a game of Connect 4
      - Error checking is handled
   - Override the depth limit for minimax by doing `--depth-limit <depth>` as a command line argument
      - `python3 minimax_player.py --depth-limit 26` will play with a depth limit of 26
   - Override the depth limit for minimax by doing `--eval-fn <fn>` as a command line argument
      - `python3 minimax_player.py --eval-fn eval_connect4_2` will use the `eval_connect4_2` evaluation function during minimax.
      - The program is advanced enough to check that the function exists AND it is a valid function for the game selected.
   - All of these arguments can be combined together

### MCTS Option
1. `python3 mcts_player.py`
   - Basic configurations (uses all defaults)
   - Select game by following prompt
   - Select who you want to play as
   - Follow prompts for making moves and good luck!
2. `python3 mcts_player.py --help`
   - Print help/usage message for seeing optional command line arguments
3. `python3 mcts_player.py [--game <game>] [--num-iters iterations] [--c c]`
   - This runs a game with MCTS with special options (changing parameters... can override the defaults).
   - Each flag/value is optional here. If you don't specify the game, it will prompt you later during the program execution
   - Set the game through the command line by doing `--game <game>`
      - `python3 mcts_player.py --game connect4` will play a game of Connect 4
      - Error checking is handled
   - Override the number of iterations MCTS does by doing `--num-iters <iterations>` as a command line argument
      - `python3 mcts_player.py --num-iters 600` will play with 600 iterations
   - Override the exploration parameter for minimax by doing `--eval-fn <fn>` as a command line argument
      - `python3 mcts_player.py --c 1.2` will use `1.2` as the exploration parameter
   - All of these arguments can be combined together

<hr>

## Recording Stats on Agent Battles
Follow this section if you want to view statistics on how agents play against each other. You have a Minimax agent battle an MCTS agent in Connect 4 or have it battle an agent that just moves randomly. The current options are `MinimaxPlayer`, `MonteCarloPlayer`, and `RandomPlayer`. All players are defined [here](https://github.com/CSC480-Group1/CSC-480/blob/main/code/games/Player.py).

### Running it
The most basic way to run the battler is to do:
```
python3 ai_battle.py <game>
```
where game is Connect 4, othello, etc. This, without any other configuration, will create "matchups" of each player against each other. We have 3 players (as mentioned above) so in total there are 6 matchups so each agent plays against each other. While waiting for the program to finish, a progress bar is displayed to let you know how it's doing and who is playing who. **_NOTE_**: Running this can take a little while (> 5 mins on slower computers) so be patient!

The default implementation runs all 6 matchups with default parameters for each player that is different per game. The default parameters per game can be found [here](https://github.com/CSC480-Group1/CSC-480/blob/f30b43fef2ad3d72399cf300c764f1229d60d68f/code/games/ai_battle.py#L75-L96). `RandomPlayer` does not have any parameters.

Once the program has finished, a file is outputted that will be in the format `data-<game>-<date>.csv`. In that CSV file are the related metrics of the game:
- `game`: what game was being played (i.e. Connect 4)
- `max`: which player was max/went first
- `min`: which player was min/went second
- `winner`: which player (min or max) won
- `max_tottime`: time max took to evaluate all of its moves
- `min_tottime`: time min took to evaluate all of its moves
- `move_count`: total moves played in the game

Here are some sample rows:
|game         |max                                                      |min                                   |winner|max_tottime       |min_tottime       |move_count|
|-------------|---------------------------------------------------------|--------------------------------------|------|------------------|------------------|----------|
|TicTacToeGame|MinimaxPlayer(eval_func=eval_tic_tac_toe_1,depth_limit=9)|MonteCarloPlayer(num_iter=500,c=1.414)|draw  |1.9572090999572538|1.08682109991787  |5         |
|TicTacToeGame|MinimaxPlayer(eval_func=eval_tic_tac_toe_1,depth_limit=9)|MonteCarloPlayer(num_iter=500,c=1.414)|draw  |2.232681200024672 |1.1953426998807117|5         |

### More Advanced Usage

For more advanced usage of the this, please view [this Colab notebook](https://colab.research.google.com/drive/1qbrKeExzzBb-K7HgdM5KGTJri61nlGLZ?usp=sharing).

<hr>

## References
- [Othello](https://en.wikipedia.org/wiki/Reversi#Othello), [C4Pop10](https://en.wikipedia.org/wiki/Connect_Four#Pop_10), and [Checkers](https://en.wikipedia.org/wiki/Draughts) game code is from a previous class Jordan Powers took (CSC 305 at Cal Poly with Professor Clint Staley). The code can be found on [GitHub](https://github.com/lost1227/CSC-305/tree/python-boardtest/assignment/python-boardtest).
- [Connect 4](https://en.wikipedia.org/wiki/Connect_Four) game code was found [here](https://gist.github.com/rex8312/c7640c96430af5209e1a) and made by Hyunsoo Park.
- Evaluation functions for Connect 4 references
   - [eval_connect4_2](https://www.scirp.org/html/1-9601415_90972.htm#f12)
   - [eval_connect4_3](https://softwareengineering.stackexchange.com/questions/263514/why-does-this-evaluation-function-work-in-a-connect-four-game-in-java) was derived from a StackOverflow post
- Evaluation functions for other games were written with help from specification from the same CSC 305 class mentioned above.
- _Minimax + Alpha-beta pruning_ and _Monte Carlo Tree Search_ algorithms were copied from our CSC 480 class with Professor Rodrigo Canaan and modified as needed.
