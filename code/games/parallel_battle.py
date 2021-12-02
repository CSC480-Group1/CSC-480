import threading
import subprocess
import json
import sys
import datetime
from pathlib import Path
try:
    import tqdm
except ModuleNotFoundError:
    tqdm = None
import csv

max_threads = 10

game_sem = threading.Semaphore(max_threads)
stdout_lock = threading.Lock()

games = {
    "checkers": ("Games.CheckersGame()", "ai_battle.MinimaxPlayer(eval_funcs.eval_checkers_1, 6)", "ai_battle.MonteCarloPlayer(num_iter=500, c=1.414)"),
    "othello": ("Games.OthelloGame()", "ai_battle.MinimaxPlayer(eval_funcs.eval_othello_1, 4)", "ai_battle.MonteCarloPlayer(num_iter=500, c=1.414)"),
    "c4pop10": ("Games.C4Pop10Game()", "ai_battle.MinimaxPlayer(eval_funcs.eval_c4pop10_1, 6)", "ai_battle.MonteCarloPlayer(num_iter=500, c=1.414)")
}

codestr = """
import ai_battle
import Games
import eval_funcs
import json
print(json.dumps(ai_battle.play_game({}, {}, {})))
"""

if len(sys.argv) < 2:
    print("No game specified")
    exit(1)


if sys.argv[1] not in games:
    print("Unknown game {}".format(sys.argv[1]))
    exit(1)

gameOpts = games[sys.argv[1]]

pairs = [
    (gameOpts[1], "ai_battle.RandomPlayer()"),
    (gameOpts[2], "ai_battle.RandomPlayer()"),
    (gameOpts[1], gameOpts[2])
]
play_count = 5

game = gameOpts[0]

dataFile = Path('./data-{}-{}.csv'.format(sys.argv[1], datetime.datetime.now().strftime('%m_%d-%H_%M')))

print("Playing", game)

def run_subgame(idx: int, outdict, game: str, player1: str, player2: str):
    with game_sem:
        result = subprocess.run([
            sys.executable,
            "-c",
            codestr.format(game, player1, player2)
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    if result.returncode != 0:
        with stdout_lock:
            print("Error running game (rc={}):".format(result.returncode))
            print("---OUTPUT---")
            print(result.stdout)
            print(result.stderr)
            print("------------")
    else:
        try:
            outdict[idx] = json.loads(result.stdout)
        except json.decoder.JSONDecodeError:
            print("Invalid output from game:")
            print("---OUTPUT---")
            print(result.stdout)
            print(result.stderr)
            print("------------")

threads = []
results = {}
i = 0

for pair in pairs:
    for _ in range(play_count):
        threads.append(threading.Thread(target=run_subgame, args=(i, results, game, pair[0], pair[1])))
        i += 1
    for _ in range(play_count):
        threads.append(threading.Thread(target=run_subgame, args=(i, results, game, pair[1], pair[0])))
        i += 1

for thread in threads:
    thread.start()

if tqdm is not None:
    pbar = tqdm.tqdm(total=(len(pairs) * 2 * play_count), desc='Simulating games')

try:
    for thread in threads:
        thread.join()
        if tqdm is not None:
            with stdout_lock:
                pbar.update()
except KeyboardInterrupt:
    print("Interrupted!")

if tqdm is not None:
    with stdout_lock:
        pbar.close()

with dataFile.open('w') as df:
    writer = csv.DictWriter(df, fieldnames=['game', 'max', 'min', 'winner', 'max_tottime', 'min_tottime', 'move_count'])
    writer.writeheader()

    for key in sorted(results):
        writer.writerow(results[key])

if tqdm is not None:
    pbar.close()
