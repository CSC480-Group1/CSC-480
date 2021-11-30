import ctypes
import platform
from pathlib import Path

_dir_path = Path(__file__).resolve().parent / "bins"

assert _dir_path.is_dir()

_boardtest_file = None
if platform.system() == "Windows":
   if platform.machine() == "AMD64":
      _boardtest_file = _dir_path / "boardtest-x64.dll"
   elif platform.machine() == "x86":
      _boardtest_file = _dir_path / "boardtest.dll"
elif platform.system() == "Linux":
   if platform.machine() == "x86_64":
      _boardtest_file = _dir_path / "boardtest.so"
   elif platform.machine() == "aarch64":
      _boardtest_file = _dir_path / "boardtest-aarch64.so"

if _boardtest_file is None:
   raise Exception("Unsupported platform")

assert _boardtest_file.is_file()

_boardtest = ctypes.CDLL(str(_boardtest_file))

class _RawData(ctypes.Structure):
   _fields_ = [
      ('data', ctypes.c_void_p),
      ('size', ctypes.c_size_t)
   ]

_boardtest.boardtest_init.argtypes = [ctypes.c_char_p]
_boardtest.boardtest_init.restype = ctypes.c_int

_boardtest.boardtest_entermove.argtypes = [ctypes.c_char_p]
_boardtest.boardtest_entermove.restype = ctypes.c_int

_boardtest.boardtest_showmove.restype = _RawData

_boardtest.boardtest_saveboard.restype = _RawData

_boardtest.boardtest_savemove.restype = _RawData

_boardtest.boardtest_getBoardKey.restype = _RawData

_boardtest.boardtest_loadboard.restype = _RawData

_boardtest.boardtest_loadmove.restype = _RawData

_boardtest.boardtest_undoMoves.argtypes = [ctypes.c_int]

_boardtest.boardtest_showboard.restype = _RawData

_boardtest.boardtest_getBinaryBoard.restype = _RawData

_boardtest.boardtest_getValidMoves.restype = _RawData

_boardtest.boardtest_getMoveHist.restype = _RawData

_boardtest.boardtest_getBoardVal.restype = ctypes.c_int

_boardtest.boardtest_free_rawdata.argtypes = [_RawData]

def _rawdataToBytes(data: _RawData):
   if data.size == 0:
      return bytes()
   dataBytes = ctypes.cast(data.data, ctypes.POINTER(ctypes.c_char))[:data.size]
   _boardtest.boardtest_free_rawdata(data)
   return dataBytes

def init(boardtype : str):
   result = _boardtest.boardtest_init(boardtype.encode('ascii'))
   if result != 0:
      print("Failed to init")
      exit(1)

def enterMove(move : str):
   res = _boardtest.boardtest_entermove(move.encode('ascii'))
   if res < 0:
      raise ValueError("Invalid move")

def getCurrMove():
   move = _boardtest.boardtest_showmove()
   decodedMove = ctypes.cast(move.data, ctypes.POINTER(ctypes.c_char))[:move.size].decode('ascii')
   _boardtest.boardtest_free_rawdata(move)
   return decodedMove

def applyMove():
   _boardtest.boardtest_applymove()


def saveBoardState():
   boardState = _boardtest.boardtest_saveboard()
   boardData = ctypes.cast(boardState.data, ctypes.POINTER(ctypes.c_char))[:boardState.size]
   _boardtest.boardtest_free_rawdata(boardState)
   return boardData

def saveRawMove():
   moveData = _boardtest.boardtest_savemove()
   moveDataByteBuff = ctypes.cast(moveData.data, ctypes.POINTER(ctypes.c_char))[:moveData.size]
   _boardtest.boardtest_free_rawdata(moveData)
   return moveDataByteBuff

def getBoardKey():
   return _rawdataToBytes(_boardtest.boardtest_getBoardKey())

def loadBoardState(boardState: bytes):
   encodedData = _RawData()
   encodedData.size = len(boardState)
   encodedData.data = ctypes.cast(ctypes.c_char_p(boardState), ctypes.c_void_p)
   _boardtest.boardtest_loadboard(encodedData)

def loadRawMove(rawMove: bytes):
   encodedData = _RawData()
   encodedData.size = len(rawMove)
   encodedData.data = ctypes.cast(ctypes.c_char_p(rawMove), ctypes.c_void_p)
   _boardtest.boardtest_loadmove(rawMove)

def undoMoves(moveCount: int):
   _boardtest.boardtest_undoMoves(moveCount)

def showBoard():
   boardState = _boardtest.boardtest_showboard()
   boardString = ctypes.cast(boardState.data, ctypes.POINTER(ctypes.c_char))[:boardState.size].decode('ascii')
   _boardtest.boardtest_free_rawdata(boardState)
   return boardString

def getBinaryBoard():
   binBoard = _boardtest.boardtest_getBinaryBoard()
   boardBytes = ctypes.cast(binBoard.data, ctypes.POINTER(ctypes.c_char))[:binBoard.size]
   _boardtest.boardtest_free_rawdata(binBoard)
   return boardBytes

def getValidMoves():
   validMoves = _boardtest.boardtest_getValidMoves()
   if(validMoves.size == 0):
      return []
   moveBuff = ctypes.cast(validMoves.data, ctypes.POINTER(ctypes.c_char))[:validMoves.size-1]
   moveStrs = [buff.decode('ascii') for buff in moveBuff.split(b'\x00')]
   _boardtest.boardtest_free_rawdata(validMoves)
   return moveStrs


def getMoveHist():
   moveHist = _boardtest.boardtest_getMoveHist()
   if(moveHist.size == 0):
      return []
   moveBuff = ctypes.cast(moveHist.data, ctypes.POINTER(ctypes.c_char))[:moveHist.size-1]
   moveStrs = [buff.decode('ascii') for buff in moveBuff.split(b'\x00')]
   _boardtest.boardtest_free_rawdata(moveHist)
   return moveStrs

def getBoardValue():
   return _boardtest.boardtest_getBoardVal()


