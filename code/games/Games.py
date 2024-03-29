from abc import ABC, abstractmethod
from Connect4 import Connect4Impl, BLACK, WHITE, NONE
import BoardTest
import struct
import copy
import io


"""

This file contains all the code needed to play a Game.

Games are divided into Python games and CGames. CGames are games
written in C++ that we use the ctype library to port over to Python.
This is done within the BoardTest.py file.

"""

class Game(ABC):
   """
   Every game must adhere to the interface provided here.

   ONLY ONE GAME AT A TIME MAY BE INITIALIZED. Call close() to be able
   to make a new Game.
   """
   _initialized = False
   def __init__(self):
      self.__valid = not Game._initialized
      if Game._initialized:
         raise Exception("Only one game at a time is supported")
      self._boardStateSynched = False
      Game._initialized = True

   @abstractmethod
   def doMove(self, move: str):
      """ Load and execute a move. """
      pass

   @abstractmethod
   def undoMoves(self, movecount: int):
      """ Undo moveCount moves. If moveCount is greater than the number of
      moves that have been executed, the board will be reset to its initial
      state. """
      pass

   @abstractmethod
   def getBoardKey(self):
      """ Get a compressed binary representation of the current board suitable
      for use in a hash table. Indended for use with a transposition table in
      minimax """
      pass

   @abstractmethod
   def showBoard(self):
      """ Get a formatted string representation of the current board, intended to be showed to a
      human. The returned string will likely contain newlines. """
      pass

   @abstractmethod
   def getValidMoves(self):
      """ Get a list of all valid move strings from the current board configuration. """
      pass

   @abstractmethod
   def getMoveHist(self):
      """ Get a list of all previously applied moves. """
      pass

   @abstractmethod
   def getPlayer(self):
      """Get the name of the current player (either "min" or "max")."""
      pass

   @abstractmethod
   def getWinner(self):
      """If the game is at a terminal state, returns the name of the winning player (either
      "min", "max", or "draw"). Otherwise, returns None."""
      pass

   @staticmethod
   def check_game_valid(func):
      """ This is a decorator to make sure the game is valid and initialized """
      def validity_fn(self, *args):
         if not self.__valid:
            raise Exception(f'Game {self} has been closed/deleted!')
         return func(self, *args)
      return validity_fn

   def close(self):
      """Deletes the game. Allows new game to be created"""
      if self.__valid:
         self.__valid = False
         Game._initialized = False

   def __del__(self):
      self.close()


class CGame(Game):
   """
   Games implemented from BoardTest.py
   """
   def __init__(self, gamestr):
      super().__init__()
      BoardTest.init(gamestr)

   @Game.check_game_valid
   def enterMove(move: str):
      """ Load a move as the 'current' move, ready to be executed. """
      BoardTest.enterMove(move)

   @Game.check_game_valid
   def applyMove():
      """ Execute the currently loaded move. """
      BoardTest.applyMove()

   @Game.check_game_valid
   def getCurrMove(self):
      """ Get the currently loaded move"""
      return BoardTest.getCurrMove()

   @Game.check_game_valid
   def doMove(self, move: str):
      """ Load and execute a move. Shorthand for enterMove() followed by
      applyMove(). """
      self._boardStateSynched = False
      BoardTest.enterMove(move)
      BoardTest.applyMove()

   @Game.check_game_valid
   def saveBoardState(self):
      """ Get the current board state as a binary blob. This can be later used
      by loadBoardState() to restore the board state. """
      return BoardTest.saveBoardState()

   @Game.check_game_valid
   def loadBoardState(self, boardState: bytes):
      """ Restore a board state saved by saveBoardState(). """
      self._boardStateSynched = False
      BoardTest.loadBoardState(boardState)

   @Game.check_game_valid
   def undoMoves(self, moveCount: int):
      self._boardStateSynched = False
      BoardTest.undoMoves(moveCount)

   @Game.check_game_valid
   def getBoardKey(self):
      """ Get a compressed binary representation of the current board suitable
      for use in a hash table. Intended for use with a transposition table in
      minimax """
      return BoardTest.getBoardKey()

   @Game.check_game_valid
   def showBoard(self):
      return BoardTest.showBoard()

   @Game.check_game_valid
   def _verifyStateSync(self):
      if not self._boardStateSynched:
         self._syncBoardState()

   @Game.check_game_valid
   def _syncBoardState(self):
      if self._boardStateSynched:
         return
      self._boardStateSynched = True
      self._parseBoardState(BoardTest.getBinaryBoard())
      self._moves = BoardTest.getValidMoves()

   @abstractmethod
   def _parseBoardState(self, binData):
      pass

   @Game.check_game_valid
   def getValidMoves(self):
      self._verifyStateSync()
      return self._moves

   @Game.check_game_valid
   def getMoveHist(self):
      return BoardTest.getMoveHist()


class CheckersGame(CGame):
   def __init__(self):
      super().__init__("CheckersBoard")

   @Game.check_game_valid
   def _parseBoardState(self, binData):
      with io.BytesIO(binData) as strm:

         dim = struct.unpack('B', strm.read(1))[0]
         self._dim = dim
         self._board = []
         for _ in range(dim-1, -1, -1):
            rowArr = []
            for _ in range(0, dim):
               rowArr.append(struct.unpack('B', strm.read(1))[0])
            self._board.append(rowArr)
         self._move = struct.unpack('B', strm.read(1))[0]

   @Game.check_game_valid
   def getWhoseMove(self):
      self._verifyStateSync()
      if self._move == 0:
         return "BLACK"
      else:
         return "WHITE"

   @Game.check_game_valid
   def getDim(self):
      """ Get the dimensions of the chess board. The board will have size
      getDim() x getDim(). """
      self._verifyStateSync()
      return self._dim

   @Game.check_game_valid
   def getPieceAtPos(self, row, col):
      """ Get the value of a piece at a certain board position. (0, 0) is in the
      upper-left corner. A dot (.) indicates no piece. A letter ("w" or "b")
      indicates the color of the piece. Capitalized letters are kinged. """
      self._verifyStateSync()

      assert row < self._dim and col < self._dim

      piece = self._board[row][col]

      pieceStr = ""

      if piece & 0x01 != 0:
         if piece & 0x02 != 0:
            pieceStr = 'w'
         else:
            pieceStr = 'b'
      else:
         pieceStr = '.'

      if piece & 0x04 != 0:
         pieceStr = pieceStr.upper()

      return pieceStr

   @Game.check_game_valid
   def getPlayer(self):
      if self.getWhoseMove() == 'BLACK':
         return 'max'
      else:
         return 'min'

   @Game.check_game_valid
   def getWinner(self):
      if len(self.getValidMoves()) != 0:
         return None

      if self.getPlayer() == "max":
         return "min"
      else:
         return "max"

class OthelloGame(CGame):
   def __init__(self):
      super().__init__("OthelloBoard")

   @Game.check_game_valid
   def _parseBoardState(self, binData):
      with io.BytesIO(binData) as strm:
         dim = struct.unpack('B', strm.read(1))[0]
         self._dim = dim
         self._board = []
         for _ in range(dim):
            rowArr = []
            for _ in range(dim):
               rowArr.append(struct.unpack('b', strm.read(1))[0])
            self._board.append(rowArr)
         self._move = struct.unpack('B', strm.read(1))[0]

   @Game.check_game_valid
   def getWhoseMove(self):
      self._verifyStateSync()
      if self._move == 0:
         return "BLACK"
      else:
         return "WHITE"

   @Game.check_game_valid
   def getDim(self):
      """ Get the dimensions of the chess board. The board will have size
      getDim() x getDim(). """
      self._verifyStateSync()
      return self._dim

   @Game.check_game_valid
   def getPieceAtPos(self, row, col):
      """ Get the value of a piece at a certain board position. (0, 0) is in the
      upper-left corner. A dot (.) indicates no piece. A letter ("W" or "B")
      indicates the color of the piece. """
      self._verifyStateSync()

      assert row < self._dim and col < self._dim

      piece = self._board[row][col]

      if piece == -1:
         return 'W'
      elif piece == 0:
         return '.'
      elif piece == 1:
         return 'B'
      else:
         raise ValueError("Unknown Othello board value (0x{:0X})".format(piece))

   @Game.check_game_valid
   def getPlayer(self):
      if self.getWhoseMove() == 'BLACK':
         return 'max'
      else:
         return 'min'

   @Game.check_game_valid
   def getWinner(self):
      if len(self.getValidMoves()) != 0:
         return None

      black_count = white_count = 0
      for row in range(self.getDim()):
         for col in range(self.getDim()):
            piece = self.getPieceAtPos(row, col)
            if piece == 'W':
               white_count += 1
            elif piece == 'B':
               black_count += 1
      if black_count > white_count:
         return 'max'
      elif white_count > black_count:
         return 'min'
      else:
         return 'draw'

class C4Pop10Game(CGame):
   class C4Pop10GameScore:
      """An object representing a player's score in C4Pop10. The score contains
      three values: safe disks, threat disks, and kept disks. A safe disc is one
      that can be removed and kept on this or a later move, with no opportunity
      for the opponent to interfere. A threat disk is a disc that the opponent
      can remove and keep unless the player does something to interfere. A kept
      disk is a disc the player has already removed and kept."""
      def __init__(self):
         self.safeDisks = 0
         self.threatDisks = 0
         self.keptDisks = 0

   def __init__(self):
      super().__init__("C4Pop10Board")

   @Game.check_game_valid
   def _parseBoardState(self, binData):
      byte = struct.iter_unpack('b', binData)
      byte = map(lambda b: b[0], byte)
      self._width = next(byte)
      self._height = next(byte)
      self._board = []
      for _ in range(self._height):
         row = []
         for _ in range(self._width):
            row.append(next(byte))
         self._board.append(row)
      assert len(self._board) == self._height
      assert len(self._board[0]) == self._width
      self._move = next(byte)

      self._redScore = C4Pop10Game.C4Pop10GameScore()
      self._yellowScore = C4Pop10Game.C4Pop10GameScore()

      self._redScore.safeDisks = next(byte)
      self._redScore.threatDisks = next(byte)
      self._redScore.keptDisks = next(byte)

      self._yellowScore.safeDisks = next(byte)
      self._yellowScore.threatDisks = next(byte)
      self._yellowScore.keptDisks = next(byte)

   @Game.check_game_valid
   def getWhoseMove(self):
      self._verifyStateSync()
      if self._move == 0:
         return "WHITE"
      else:
         return "BLACK"

   @Game.check_game_valid
   def getBoardDimensions(self):
      """ Get the dimensions of the checkers board. The return value is a
      tuple of (width, height)."""
      self._verifyStateSync()
      return (self._width, self._height)

   @Game.check_game_valid
   def getPieceAtPos(self, row, col):
      """Get the value of a piece at a certain board position. (0, 0) is in the
      upper-left corner. A dot (.) indicates no piece. A letter ("R" or "Y")
      indicates the color of the piece. """
      self._verifyStateSync()

      assert row < self._height and col < self._width

      piece = self._board[row][col]

      if piece & 0x01 != 0:
         if piece & 0x02 != 0:
            return "R"
         else:
            return "Y"
      else:
         return "."

   @Game.check_game_valid
   def getRedScore(self):
      """Gets the score of the red player. Returns a C4Pop10GameScore object."""
      self._verifyStateSync()
      return self._redScore

   @Game.check_game_valid
   def getYellowScore(self):
      """Gets the score of the yellow player. Returns a C4Pop10GameScore object."""
      self._verifyStateSync()
      return self._yellowScore

   @Game.check_game_valid
   def getPlayer(self):
      if self.getWhoseMove() == 'WHITE':
         return 'max'
      else:
         return 'min'

   @Game.check_game_valid
   def getWinner(self):
      if len(self.getValidMoves()) != 0:
         return None

      yellow_score = self.getYellowScore()
      red_score = self.getRedScore()

      if yellow_score.keptDisks == 10:
         return 'max'
      elif red_score.keptDisks == 10:
         return 'min'
      else:
         raise ValueError("Somehow, someone won without keeping 10 disks (which is not possible)")


class Connect4(Game):
   def __init__(self):
      super().__init__()
      self.game = Connect4Impl()
      self.game_states = [self.getBoardCopy()]
      self.saved_column = None
      self.history = []

   @Game.check_game_valid
   def resetGame(self):
      self.game.reset_game()
      self.game_states = [self.getBoardCopy()]
      self.history = []

   @Game.check_game_valid
   def printBoard(self):
      return self.game.printBoard()

   @Game.check_game_valid
   def showBoard(self):
      return self.game.getBoardRepr()

   @Game.check_game_valid
   def getBoardCopy(self):
      return copy.deepcopy(self.game.board)

   @Game.check_game_valid
   def getWhoseMove(self):
      return self.game.getWhoseMove()

   @Game.check_game_valid
   def getPlayer(self):
      if self.getWhoseMove() == 'BLACK':
         return 'max'
      else:
         return 'min'

   @Game.check_game_valid
   def getWinner(self):
      if len(self.getValidMoves()) != 0:
         return None

      if self.game.getWinner() == BLACK:
         return "max"
      return "min"

   @Game.check_game_valid
   def getDimensions(self):
      return (self.game.rows, self.game.cols)

   @Game.check_game_valid
   def doMove(self, column):
      try:
         int_col = int(column)
         success = self.game.insert(int_col)
         if success:
            self.game_states.append(self.getBoardCopy())
            self.history.append(int_col)
      except ValueError:
         print('Please provide a valid column NUMBER')

   @Game.check_game_valid
   def applyMove(self):
      self.doMove(self.saved_column)

   @Game.check_game_valid
   def enterMove(self, move):
      self.saved_column = move

   @Game.check_game_valid
   def getCurrMove(self):
      return self.saved_column

   @Game.check_game_valid
   def getValidMoves(self):
      return self.game.getValidMoves()

   @Game.check_game_valid
   def getPieceAtPos(self, row, col):
      return self.game.board[row][col]

   @Game.check_game_valid
   def saveBoardState(self):
      return copy.deepcopy(self.history)

   @Game.check_game_valid
   def loadBoardState(self, boardHistory):
      self.resetGame()
      for val in boardHistory:
         self.doMove(val)
      self.printBoard()

   @Game.check_game_valid
   def undoMoves(self, movesToUndo):
      # Can't go past first board state
      goBackTo = max(1, 1 + len(self.history) - movesToUndo)
      self.game_states = self.game_states[:goBackTo]
      self.game.board = copy.deepcopy(self.game_states[-1])
      self.game.turn = BLACK if (goBackTo - 1) % 2 == 0 else WHITE
      self.history = self.history[:goBackTo - 1]
      self.game.game_over = self.game.checkForWin()

   @Game.check_game_valid
   def getMoveHist(self):
      return copy.deepcopy(self.history)

   @Game.check_game_valid
   def getBoardKey(self):
      return str(self.game.board)

   @Game.check_game_valid
   def getTurn(self):
      return self.game.get_turn()

   @Game.check_game_valid
   def getNextTurn(self):
      curr_turn = self.game.get_turn()
      return BLACK if curr_turn == WHITE else WHITE

"""Reimport TicTacToeGame so we can do: from Games import *"""
try:
   from tictactoe import TicTacToeGame
   TicTacToeGame = TicTacToeGame
except ModuleNotFoundError:
   TicTacToeGame = None
