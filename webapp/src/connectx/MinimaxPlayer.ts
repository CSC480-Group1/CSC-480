import { Player } from "./ConnectX";
import {
  BLACK,
  BLACK_PLAYER,
  ConnectXImpl,
  NONE,
  WHITE,
  WHITE_PLAYER,
} from "./ConnectXImpl";

export class MinimaxPlayer implements Player {
  disableMove = true;
  automated = true;
  inDecision = false;

  minimax(
    game: ConnectXImpl,
    alpha: number,
    beta: number,
    depthLimit = 0
  ): number {
    const currentPlayer = game.getWhoseMove();
    const validMoves = game.getValidMoves();

    if (validMoves.length === 0 || depthLimit === 0) {
      const utilityScore = this.eval_connect4_2(game);
      return utilityScore;
    }

    let bestScore = currentPlayer == BLACK_PLAYER ? -Infinity : Infinity;
    for (const successiveMove of validMoves) {
      game.insert(successiveMove);
      const moveScore = this.minimax(game, alpha, beta, depthLimit - 1);
      game.undoLastMove();

      if (currentPlayer === BLACK_PLAYER) {
        bestScore = Math.max(bestScore, moveScore);
        if (moveScore >= beta) {
          return moveScore;
        }
        alpha = Math.max(alpha, moveScore);
      } else {
        bestScore = Math.min(bestScore, moveScore);
        if (moveScore <= alpha) {
          return moveScore;
        }
        beta = Math.min(beta, moveScore);
      }
    }

    return bestScore;
  }

  // https://www.scirp.org/html/1-9601415_90972.htm#f12
  // https://github.dev/Qtrain/Java/blob/master/src/unfinishedProjects/connectfour/Board.java
  evaluationTable = [
    [3, 4, 5, 7, 5, 4, 3],
    [4, 6, 8, 10, 8, 6, 4],
    [5, 8, 11, 13, 11, 8, 5],
    [5, 8, 11, 13, 11, 8, 5],
    [4, 6, 8, 10, 8, 6, 4],
    [3, 4, 5, 7, 5, 4, 3],
  ];
  eval_connect4_2(game: ConnectXImpl): number {
    const utility = 138;
    if (game.getWinner() !== NONE) {
      return game.getWhoseMove() == BLACK_PLAYER ? utility * 2 : -(utility * 2);
    } else if (game.getValidMoves().length === 0) {
      return utility;
    }

    const max_rows = game.board[0].length;
    const max_cols = game.board.length;
    const board = game.board;
    let sum = 0;
    for (let i = 0; i < max_cols; i++) {
      for (let j = 0; j < max_rows; j++) {
        if (board[i][j] == BLACK) sum += this.evaluationTable[j][i];
        else if (board[i][j] != NONE) sum -= this.evaluationTable[j][i];
      }
    }
    return utility + sum;
  }

  connectXUtility(game: ConnectXImpl, depth: number): number {
    let score;
    const winner = game.checkForWin();
    if (winner === BLACK) {
      score = 1.0;
    } else if (winner === WHITE) {
      score = -1.0;
    } else {
      score = 0;
    }

    return score * (1 / (1 + depth));
  }

  DEPTH_LIMIT = 4;

  onMoveReady(_: number, game: ConnectXImpl): number {
    const currentPlayer = game.getWhoseMove();
    const validMoves = game.getValidMoves();

    if (validMoves.length === 0) {
      alert("No move to be made...");
      return -1;
    }

    let bestMoves: Array<number> = [];
    let bestScore = currentPlayer == BLACK_PLAYER ? -Infinity : Infinity;

    for (const move of validMoves) {
      game.insert(move);
      let minimaxScore = this.minimax(
        game,
        -Infinity,
        Infinity,
        this.DEPTH_LIMIT
      );
      game.undoLastMove();

      minimaxScore = Math.round(minimaxScore * 100000);

      if (bestMoves.length === 0) {
        bestMoves.push(move);
        bestScore = minimaxScore;
      } else if (currentPlayer === BLACK_PLAYER && bestScore < minimaxScore) {
        bestScore = minimaxScore;
        bestMoves = [move];
      } else if (currentPlayer === WHITE_PLAYER && bestScore > minimaxScore) {
        bestScore = minimaxScore;
        bestMoves = [move];
      } else if (bestScore === minimaxScore) {
        bestMoves.push(move);
      }
    }

    return bestMoves[Math.floor(Math.random() * bestMoves.length)];
    // return bestMove[0];
  }
}
