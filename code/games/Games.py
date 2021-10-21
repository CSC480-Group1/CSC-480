from abc import ABC, abstractmethod
from Connect4 import Connect4Impl, RED, YELLOW, NONE
import BoardTest
import struct
import copy
import io


class Game(ABC):
   _initialized = False
   def __init__(self):
      if Game._initialized:
         raise Exception("Only one game at a time is supported")
      self._boardStateSynched = False
      Game._initialized = True


class CGame(Game):
   def __init__(self, gamestr):
      super().__init__()
      BoardTest.init(gamestr)

   def enterMove(self, move: str):
      BoardTest.enterMove(move)

   def applyMove(self):
      BoardTest.applyMove()

   def getCurrMove(self):
      return BoardTest.getCurrMove()

   def doMove(self, move: str):
      self._boardStateSynched = False
      BoardTest.enterMove(move)
      BoardTest.applyMove()

   def saveBoardState(self):
      return BoardTest.saveBoardState()
   
   def loadBoardState(self, boardState: bytes):
      self._boardStateSynched = False
      BoardTest.loadBoardState(boardState)

   def undoMoves(self, moveCount: int):
      self._boardStateSynched = False
      BoardTest.undMoves(moveCount)

   def showBoard(self):
      return BoardTest.showBoard()

   def getValidMoves(self):
      return BoardTest.getValidMoves()
   
   def getMoveHist(self):
      return BoardTest.getMoveHist()



class CheckersGame(CGame):
   def __init__(self):
      super().__init__("CheckersBoard")

   def _parseBoardState(self):
      binData = BoardTest.getBinaryBoard()
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

   def _verifyStateSync(self):
      if not self._boardStateSynched:
         self._parseBoardState()
         self._boardStateSynched = True

   def getWhoseMove(self):
      self._verifyStateSync()
      if self._move == 0:
         return "BLACK"
      else:
         return "WHITE"

   def getDim(self):
      self._verifyStateSync()
      return self._dim
   
   def getPieceAtPos(self, row, col):
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

class OthelloGame(CGame):
   def __init__(self):
      super().__init__("OthelloBoard")

   def _parseBoardState(self):
      binData = BoardTest.getBinaryBoard()
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

   def _verifyStateSync(self):
      if not self._boardStateSynched:
         self._parseBoardState()
         self._boardStateSynched = True

   def getWhoseMove(self):
      self._verifyStateSync()
      if self._move == 0:
         return "BLACK"
      else:
         return "WHITE"

   def getDim(self):
      self._verifyStateSync()
      return self._dim
   
   def getPieceAtPos(self, row, col):
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

class C4Pop10Game(CGame):
   class C4Pop10GameScore:
      def __init__(self):
         self.safeDisks = 0
         self.threatDisks = 0
         self.keptDisks = 0

   def __init__(self):
      super().__init__("C4Pop10Board")

   def _parseBoardState(self):
      binData = BoardTest.getBinaryBoard()
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

   def _verifyStateSync(self):
      if not self._boardStateSynched:
         self._parseBoardState()
         self._boardStateSynched = True

   def getWhoseMove(self):
      self._verifyStateSync()
      if self._move == 0:
         return "YELLOW"
      else:
         return "RED"
   
   def getBoardDimensions(self):
      self._verifyStateSync()
      return (self._width, self._height)
   
   def getPieceAtPos(self, row, col):
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

   def getRedScore(self):
      self._verifyStateSync()
      return self._redScore

   def getYellowScore(self):
      self._verifyStateSync()
      return self._yellowScore


class Connect4(Game):
   def __init__(self):
      super().__init__()
      self.game = Connect4Impl()
      self.game_states = [self.getBoardCopy()]
      self.saved_column = None
      self.history = []

   def showBoard(self):
      return self.game.printBoard()

   def getBoardCopy(self):
      return copy.deepcopy(self.game.board)

   def getWhoseMove(self):
      return self.game.getWhoseMove()

   def getDimensions(self):
      return (self.game.rows, self.game.cols)

   def doMove(self, column):
      try:
         int_col = int(column)
         success = self.game.insert(int_col)
         if success:
            self.game_states.append(self.getBoardCopy())
            self.history.append(int_col)
      except ValueError:
         print('Please provide a valid column NUMBER')

   def applyMove(self):
      self.doMove(self.saved_column)

   def enterMove(self, move):
      self.saved_column = move

   def getCurrMove(self):
      return self.saved_column

   def getValidMoves(self):
      return self.game.getValidMoves()

   def getPieceAtPos(self, row, col):
      return self.game.board[row][col]

   def saveBoardState(self):
      print('METHOD NOT IMPLEMENTED')

   def loadBoardState(self, boardState):
      print('METHOD NOT IMPLEMENTED')

   def undoMoves(self, movesToUndo):
      # Can't go past first board state
      goBackTo = max(1, 1 + len(self.history) - movesToUndo)
      self.game_states = self.game_states[:goBackTo]
      self.game.board = self.game_states[-1]
      self.game.turn = RED if (goBackTo - 1) % 2 == 0 else YELLOW
      self.history = self.history[:goBackTo - 1]

