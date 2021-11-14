import { Player } from "./ConnectX";
import { BLACK, BLACK_PLAYER, ConnectXImpl, WHITE, WHITE_PLAYER } from "./ConnectXImpl";

const transpositionTable = new Map<string, number>();

const ttGet = (board: Array<Array<string>>, depth?: number): number | undefined => {
  return transpositionTable.get(board.toString());
};

const ttPut = (board: Array<Array<string>>, score: number, depth?: number): void => {
  transpositionTable.set(board.toString(), score);
};

export class MinimaxPlayer implements Player {
  disableMove = true;
  automated = true;
  inDecision = false;

  minimax(game: ConnectXImpl, alpha: number, beta: number, depth=0): number {
    const currentPlayer = game.getWhoseMove();
    const validMoves = game.getValidMoves();

    const tempScore = ttGet(game.board);
    if (tempScore) {
      return tempScore;
    }

    if (validMoves.length === 0) {
      const utilityScore = this.connectXUtility(game, depth);
      ttPut(game.board, utilityScore);
      return utilityScore;
    }

    let bestScore = currentPlayer == BLACK_PLAYER ? -Infinity : Infinity;
    for (const successiveMove of validMoves) {
      game.insert(successiveMove);
      const moveScore = this.minimax(game, alpha, beta, depth + 1);
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
      let minimaxScore = this.minimax(game, -Infinity, Infinity);
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