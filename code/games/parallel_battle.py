import threading
import subprocess
import sys
from Games import Game
from Player import Player
from ai_battle import AIBattle, AllPlayerBattle
import pickle
import queue

"""

Same as ai_battle.py stuff but runs bouts in parallel.

"""

try:
    import tqdm
except ModuleNotFoundError:
    tqdm = None

try:
    from tictactoe import TicTacToeGame
except ModuleNotFoundError:
    TicTacToeGame = None


max_subprocesses = 10

game_sem = threading.Semaphore(max_subprocesses)
stdout_lock = threading.Lock()

codestr = """
import pickle
import sys
from ai_battle import AIBattle
args = pickle.load(sys.stdin.buffer)
result = AIBattle._play_game(args[0](), args[1], args[2], args[3])
pickle.dump(result, sys.stdout.buffer)
"""

class ParallelBattle(AIBattle):
    def __init__(self, game: Game, p1: Player, p2: Player, update=print, move_limit=300, play_count=5) -> None:
        super().__init__(game, p1, p2, update, move_limit, play_count)
        self.__results = queue.Queue()

    def __run_subgame(self, maxPlayer, minPlayer):
        pickled_args = pickle.dumps((self.game.__class__, self.move_limit, maxPlayer, minPlayer))
        with game_sem:
            subproc = subprocess.Popen([
                sys.executable,
                "-c",
                codestr.format(
                    f"{self.game.__class__.__name__}()",
                    str(maxPlayer),
                    str(minPlayer),
                    self.move_limit
                )
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

            sub_stdout, sub_stderr = subproc.communicate(input=pickled_args)

        if subproc.returncode != 0:
            with stdout_lock:
                print("Error running game (rc={}):".format(subproc.returncode))
                print("---OUTPUT---")
                print(sub_stdout)
                print(sub_stderr.decode('utf8'))
                print("------------")
        else:
            try:
                self.__results.put(pickle.loads(sub_stdout))
            except pickle.UnpicklingError as e:
                with stdout_lock:
                    print("Invalid output from game:")
                    print("---OUTPUT---")
                    print(sub_stdout)
                    print(sub_stderr.decode('utf8'))
                    print("------------")


    def go(self):
        threads = []
        for _ in range(self.play_count):
            threads.append(threading.Thread(target=self.__run_subgame, args=(self.p1, self.p2)))
        for _ in range(self.play_count):
            threads.append(threading.Thread(target=self.__run_subgame, args=(self.p2, self.p1)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            if not self.__results.empty():
                # If the subprocess doesn't finish (an exception occurs or the user interrupts
                # the program), we don't have results to dequeue
                self.update(self.__results.get())

        assert self.__results.empty()

class ParallelAllPlayerBattle(AllPlayerBattle):
    def __init__(self, game_choice: str, write_to_csv=True, move_limit=300, play_count=5,
            players=None, use_tqdm=True) -> None:
        super().__init__(game_choice, write_to_csv=write_to_csv, move_limit=move_limit,
            play_count=play_count, players=players, use_tqdm=use_tqdm)

        self.__update_lock = threading.Lock()

    def __update_res(self, res):
        if self.use_tqdm:
            with stdout_lock:
                self.pbar.update()
        if self.writer is not None:
            with self.__update_lock:
                self.writer.write_result(res)

    def battle(self):
        # Setup
        game = self.game_class()
        if self.writer is not None:
            self.writer.open()
        if self.use_tqdm and not self.pbar:
            with stdout_lock:
                self.pbar = tqdm.tqdm(total=(len(self.game_matchups) * 2 * self.play_count), desc='Simulating games')

        threads = []

        for p1, p2 in self.game_matchups:
            new_battle = ParallelBattle(game, p1, p2, update=self.__update_res,
                move_limit=self.move_limit, play_count=self.play_count)
            threads.append(threading.Thread(target=new_battle.go))

        for thread in threads:
            thread.start()

        try:
            for thread in threads:
                thread.join()
        except InterruptedError:
            print("Interrupted!")

        if self.writer is not None:
            self.writer.close()

        if self.use_tqdm:
            with stdout_lock:
                self.pbar.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No game specified")
        exit(1)

    if TicTacToeGame is None and sys.argv[1] == "tic tac toe":
        print("Tic tac toe requires numpy, install with <python3 -m pip install numpy>")
        exit(1)

    all_battles = ParallelAllPlayerBattle(sys.argv[1], use_tqdm=(tqdm is not None))

    all_battles.battle()
