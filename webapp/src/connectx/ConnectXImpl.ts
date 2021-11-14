import { chain, groupby } from "./itertools";

export const NONE = ".";
export const BLACK = "B";
export const WHITE = "W";
export const BLACK_PLAYER = "BLACK";
export const WHITE_PLAYER = "WHITE";

const zip = (...rows: any[]) =>
  [...rows[0]].map((_, c) => rows.map((row) => row[c]));

function genBoard(rows: number, columns: number): Array<Array<string>> {
  const board: Array<Array<string>> = [];

  for (let i = 0; i < columns; i++) {
    board.push([]);
    for (let j = 0; j < rows; j++) {
      board[i].push(NONE);
    }
  }

  return board;
}

export class ConnectXImpl {
  cols: number;
  rows: number;
  win: number;
  gameOver: boolean;
  board: Array<Array<string>>;
  turn: string;
  moveHistory: Array<number>;

  constructor(cols = 4, rows = 4, requiredToWin = 3) {
    this.cols = cols;
    this.rows = rows;
    this.win = requiredToWin;
    this.gameOver = false;
    this.board = genBoard(rows, cols);
    this.turn = BLACK;
    this.moveHistory = [];
  }

  resetGame(): void {
    this.turn = BLACK;
    this.board = genBoard(this.rows, this.cols);
    this.gameOver = false;
    this.moveHistory = [];
  }

  stop(): void {
    this.gameOver = true;
  }

  insert(column: number, shadow = false): boolean {
    if (this.gameOver) {
      alert("Game is over!");
      return false;
    }

    const color = this.turn;

    if (column < 0 || column >= this.cols) {
      alert(`Invalid column given: ${column}. Choose between 0 and ${this.cols - 1}`);
      return false;
    }

    const c = this.board[column];
    if (c[0] != NONE) {
      if (!shadow) {
        // this.printBoard();
        alert(`Column ${column} is full`);
      }

      return false;
    }

    let i = c.length - 1;
    while (c[i] != NONE) {
      i--;
    }

    if (!shadow) {
      c[i] = color;
      this.moveHistory.push(column);
      const have_won = this.checkForWin();
      if (have_won != NONE) {
        this.gameOver = true;
      }
      this.turn = this.turn == BLACK ? WHITE : BLACK;
    }

    return true;
  }

  getWhoseMove(): string {
    return this.turn == BLACK ? BLACK_PLAYER : WHITE_PLAYER;
  }

  checkForWin(): string {
    const w = this.getWinner();
    return w;
  }

  getWinningPlayer(): string {
    const w = this.checkForWin();
    if (w != NONE) {
      return w == BLACK ? BLACK_PLAYER : WHITE_PLAYER;
    }

    return "None";
  }

  getWinner(): string {
    const lines = [
      this.board,
      zip(...this.board),
      diagonalsPos(this.board, this.cols, this.rows),
      diagonalsNeg(this.board, this.cols, this.rows),
    ];

    for (const line of chain(...lines)) {
      for (const [color, group] of groupby(line)) {
        const groupArr = Array.from(group);
        if (color != NONE && Array.from(groupArr).length >= this.win) {
          return color as string;
        }
      }
    }

    return NONE;
  }

  undoLastMove(): void {
    console.log(this.moveHistory);
    const moveRemoved = this.moveHistory.pop();
    if (moveRemoved === undefined) {
      return;
    }

    const c = this.board[moveRemoved];
    let i = c.length - 1;
    while (c[i] != NONE && i > 0) {
      i--;
    }

    let turnFound: string;
    if (c[i] === NONE) {
      turnFound = c[i + 1];
      c[i + 1] = NONE;
    } else {
      turnFound = c[i];
      c[i] = NONE;
    }

    this.turn = turnFound;
    this.gameOver = false;
  }

  getValidMoves(): Array<number> {
    if (this.gameOver) {
      return [];
    }

    const validMoves = [...Array(this.cols).keys()].filter((col) =>
      this.insert(col, true)
    );
    return validMoves;
  }

  getBoardRepr(): string {
    let string = [...Array(this.cols).keys()].map(String).join("  ") + "\n";
    for (let y = 0; y < this.rows; y++) {
      const board_row = [];
      for (let x = 0; x < this.cols; x++) {
        board_row.push(String(this.board[x][y]));
      }
      string += board_row.join("  ") + "\n";
    }

    return string;
  }

  printBoard(): void {
    console.log(this.getBoardRepr());
  }

  copy(): ConnectXImpl {
    const newGame = new ConnectXImpl(this.cols, this.rows, this.win);
    newGame.turn = this.turn;
    newGame.gameOver = this.gameOver;
    newGame.board = JSON.parse(JSON.stringify(this.board)); 
    newGame.moveHistory = [...this.moveHistory];
    return newGame;
  }

  static getGameFromHistory(
    history: Array<number>,
    ...args: Array<any>
  ): ConnectXImpl {
    const game = new ConnectXImpl(...args);
    for (const move of history) {
      game.insert(move);
    }

    return game;
  }
}

function diagonalsPos(
  matrix: Array<Array<string>>,
  cols: number,
  rows: number
) {
  const diagonals: Array<Array<Array<number>>> = [];
  for (let i = 0; i < cols + rows - 1; i++) {
    diagonals.push([]);
    for (let j = 0; j < cols; j++) {
      diagonals[i].push([j, i - j]);
    }
  }

  const diagonalVals: Array<Array<string>> = [];
  for (const diagRow of diagonals) {
    const newArr: Array<string> = [];
    diagonalVals.push(newArr);
    for (const [i, j] of diagRow) {
      if (i >= 0 && j >= 0 && i < cols && j < rows) {
        newArr.push(matrix[i][j]);
      }
    }
  }

  return diagonalVals;
}

function diagonalsNeg(
  matrix: Array<Array<string>>,
  cols: number,
  rows: number
) {
  const diagonals: Array<Array<Array<number>>> = [];
  for (let i = 0; i < cols + rows - 1; i++) {
    diagonals.push([]);
    for (let j = 0; j < cols; j++) {
      diagonals[i].push([j, i - cols + j + 1]);
    }
  }

  const diagonalVals: Array<Array<string>> = [];
  for (const diagRow of diagonals) {
    const newArr: Array<string> = [];
    diagonalVals.push(newArr);
    for (const [i, j] of diagRow) {
      if (i >= 0 && j >= 0 && i < cols && j < rows) {
        newArr.push(matrix[i][j]);
      }
    }
  }

  return diagonalVals;
}