```python
%run -i ../games/minimax_player.py
```

    Game options:
      1) Checkers
      2) Othello
      3) C4Pop10
      4) Tic Tac Toe
    > 1
    Play as black or white? (n for no player)
    (b/w/n)> b
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  w  .  w  .  
    F  .  w  .  w  .  w  .  w  
    E  .  .  .  .  .  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  b  .  b  .  b  .  
    B  .  b  .  b  .  b  .  b  
    A  b  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) C1 -> D2 (-20)
      2) C3 -> D2 (-20)
      3) C3 -> D4 (-20)
      4) C5 -> D4 (-20)
      5) C5 -> D6 (-20)
      6) C7 -> D6 (-20)
      7) C7 -> D8 (-20)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  w  .  w  .  
    F  .  w  .  w  .  w  .  w  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  .  .  .  
    C  .  .  b  .  b  .  b  .  
    B  .  b  .  b  .  b  .  b  
    A  b  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays F6 -> E5
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  w  .  w  .  
    F  .  w  .  w  .  .  .  w  
    E  .  .  .  .  w  .  .  .  
    D  .  b  .  .  .  .  .  .  
    C  .  .  b  .  b  .  b  .  
    B  .  b  .  b  .  b  .  b  
    A  b  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) B2 -> C1 (-20)
      2) C3 -> D4 (-120)
      3) C5 -> D4 (-120)
      4) C5 -> D6 (-20)
      5) C7 -> D6 (-20)
      6) C7 -> D8 (-20)
      7) D2 -> E1 (-20)
      8) D2 -> E3 (-20)
    > 2
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  w  .  w  .  
    F  .  w  .  w  .  .  .  w  
    E  .  .  .  .  w  .  .  .  
    D  .  b  .  b  .  .  .  .  
    C  .  .  .  .  b  .  b  .  
    B  .  b  .  b  .  b  .  b  
    A  b  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays E5 -> C3
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  w  .  w  .  
    F  .  w  .  w  .  .  .  w  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  .  .  .  
    C  .  .  w  .  b  .  b  .  
    B  .  b  .  b  .  b  .  b  
    A  b  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) B2 -> D4 (-120)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  w  .  w  .  
    F  .  w  .  w  .  .  .  w  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  b  .  .  .  .  
    C  .  .  .  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  b  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays F4 -> E3
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  w  .  w  .  
    F  .  w  .  .  .  .  .  w  
    E  .  .  w  .  .  .  .  .  
    D  .  b  .  b  .  .  .  .  
    C  .  .  .  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  b  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) D2 -> F4 (-120)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  w  .  w  .  
    F  .  w  .  b  .  .  .  w  
    E  .  .  .  .  .  .  .  .  
    D  .  .  .  b  .  .  .  .  
    C  .  .  .  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  b  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays G5 -> E3
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  .  .  w  .  
    F  .  w  .  .  .  .  .  w  
    E  .  .  w  .  .  .  .  .  
    D  .  .  .  b  .  .  .  .  
    C  .  .  .  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  b  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) A1 -> B2 (-120)
      2) A3 -> B2 (-120)
      3) B4 -> C3 (-20)
      4) C5 -> D6 (-20)
      5) C7 -> D6 (-20)
      6) C7 -> D8 (-20)
      7) D4 -> E5 (-20)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  w  .  .  .  w  .  
    F  .  w  .  .  .  .  .  w  
    E  .  .  w  .  .  .  .  .  
    D  .  .  .  b  .  .  .  .  
    C  .  .  .  .  b  .  b  .  
    B  .  b  .  b  .  b  .  b  
    A  .  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays G3 -> F4
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  w  .  
    F  .  w  .  w  .  .  .  w  
    E  .  .  w  .  .  .  .  .  
    D  .  .  .  b  .  .  .  .  
    C  .  .  .  .  b  .  b  .  
    B  .  b  .  b  .  b  .  b  
    A  .  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) B2 -> C1 (-120)
      2) B2 -> C3 (-120)
      3) B4 -> C3 (-120)
      4) C5 -> D6 (-120)
      5) C7 -> D6 (-120)
      6) C7 -> D8 (-520)
      7) D4 -> E5 (-120)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  w  .  
    F  .  w  .  w  .  .  .  w  
    E  .  .  w  .  .  .  .  .  
    D  .  .  .  b  .  .  .  .  
    C  b  .  .  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  .  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays G7 -> F6
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  w  .  w  .  w  .  w  
    E  .  .  w  .  .  .  .  .  
    D  .  .  .  b  .  .  .  .  
    C  b  .  .  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  .  .  b  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) A3 -> B2 (-220)
      2) B4 -> C3 (-120)
      3) C1 -> D2 (-120)
      4) C5 -> D6 (-120)
      5) C7 -> D6 (-120)
      6) C7 -> D8 (-220)
      7) D4 -> E5 (-120)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  w  .  w  .  w  .  w  
    E  .  .  w  .  .  .  .  .  
    D  .  .  .  b  .  .  .  .  
    C  b  .  .  .  b  .  b  .  
    B  .  b  .  b  .  b  .  b  
    A  .  .  .  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays F8 -> E7
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  w  .  w  .  w  .  .  
    E  .  .  w  .  .  .  w  .  
    D  .  .  .  b  .  .  .  .  
    C  b  .  .  .  b  .  b  .  
    B  .  b  .  b  .  b  .  b  
    A  .  .  .  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) B2 -> C3 (-220)
      2) B4 -> C3 (-220)
      3) C1 -> D2 (-520)
      4) C5 -> D6 (-620)
      5) C7 -> D6 (-320)
      6) C7 -> D8 (-420)
      7) D4 -> E5 (-320)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  w  .  w  .  w  .  .  
    E  .  .  w  .  .  .  w  .  
    D  .  .  .  b  .  .  .  .  
    C  b  .  b  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  .  .  .  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays F6 -> E5
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  w  .  w  .  .  .  .  
    E  .  .  w  .  w  .  w  .  
    D  .  .  .  b  .  .  .  .  
    C  b  .  b  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  .  .  .  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) D4 -> F6 (-220)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  w  .  w  .  b  .  .  
    E  .  .  w  .  .  .  w  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  b  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  .  .  .  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays F2 -> E1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  w  .  w  .  .  .  w  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  b  .  b  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  .  .  .  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) C1 -> D2 (-220)
      2) C3 -> D2 (-120)
      3) C3 -> D4 (-120)
      4) C5 -> D4 (-420)
      5) C5 -> D6 (-320)
      6) C7 -> D6 (-120)
      7) C7 -> D8 (-120)
      8) F6 -> G5 (-120)
      9) F6 -> G7 (-120)
    > 4
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  w  .  w  .  .  .  w  .  
    D  .  .  .  b  .  .  .  .  
    C  b  .  b  .  .  .  b  .  
    B  .  .  .  b  .  b  .  b  
    A  .  .  .  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays E3 -> C5 -> A3
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  w  .  .  .  .  .  w  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  b  .  .  .  b  .  
    B  .  .  .  .  .  b  .  b  
    A  .  .  W  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) A5 -> B4 (-420)
      2) B6 -> C5 (-520)
      3) C1 -> D2 (-520)
      4) C3 -> D2 (-520)
      5) C3 -> D4 (-520)
      6) C7 -> D6 (-520)
      7) C7 -> D8 (-520)
      8) F6 -> G5 (-420)
      9) F6 -> G7 (-420)
    > 2
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  w  .  .  .  .  .  w  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  b  .  b  .  b  .  
    B  .  .  .  .  .  .  .  b  
    A  .  .  W  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays E7 -> D8
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  w  .  .  .  .  .  .  .  
    D  .  .  .  .  .  .  .  w  
    C  b  .  b  .  b  .  b  .  
    B  .  .  .  .  .  .  .  b  
    A  .  .  W  .  b  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) A5 -> B4 (-720)
      2) A5 -> B6 (-620)
      3) A7 -> B6 (-620)
      4) C1 -> D2 (-620)
      5) C3 -> D2 (-620)
      6) C3 -> D4 (-620)
      7) C5 -> D4 (-620)
      8) C5 -> D6 (-620)
      9) C7 -> D6 (-520)
      10) F6 -> G5 (-620)
      11) F6 -> G7 (-620)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  w  .  .  .  .  .  .  .  
    D  .  .  .  .  .  .  .  w  
    C  b  .  b  .  b  .  b  .  
    B  .  .  .  b  .  .  .  b  
    A  .  .  W  .  .  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays D8 -> B6
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  w  .  .  .  .  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  b  .  b  .  .  .  
    B  .  .  .  b  .  w  .  b  
    A  .  .  W  .  .  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) B8 -> C7 (-920)
      2) C1 -> D2 (-820)
      3) C3 -> D2 (-1120)
      4) C3 -> D4 (-920)
      5) C5 -> D4 (-920)
      6) C5 -> D6 (-1020)
      7) F6 -> G5 (-920)
      8) F6 -> G7 (-920)
    > 3
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  w  .  .  .  .  .  .  .  
    D  .  b  .  .  .  .  .  .  
    C  b  .  .  .  b  .  .  .  
    B  .  .  .  b  .  w  .  b  
    A  .  .  W  .  .  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays E1 -> C3 -> A5
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  .  .  b  .  .  .  
    B  .  .  .  .  .  w  .  b  
    A  .  .  W  .  W  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) B8 -> C7 (-1120)
      2) C1 -> D2 (-1120)
      3) C5 -> D4 (-1120)
      4) C5 -> D6 (-1120)
      5) F6 -> G5 (-1120)
      6) F6 -> G7 (-1120)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  w  .  b  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  .  .  b  .  b  .  
    B  .  .  .  .  .  w  .  .  
    A  .  .  W  .  W  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays F4 -> E5
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  w  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  .  .  b  .  b  .  
    B  .  .  .  .  .  w  .  .  
    A  .  .  W  .  W  .  b  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) A7 -> B8 (-1420)
      2) C1 -> D2 (-1120)
      3) C5 -> D4 (-1320)
      4) C5 -> D6 (-1220)
      5) C7 -> D6 (-1220)
      6) C7 -> D8 (-1220)
      7) F6 -> G5 (-1120)
      8) F6 -> G7 (-1020)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  w  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  .  .  b  .  b  .  
    B  .  .  .  .  .  w  .  b  
    A  .  .  W  .  W  .  .  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays B6 -> A7
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  w  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  .  .  b  .  b  .  
    B  .  .  .  .  .  .  .  b  
    A  .  .  W  .  W  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) C1 -> D2 (-1420)
      2) C5 -> D4 (-1520)
      3) C5 -> D6 (-1420)
      4) C7 -> D6 (-1420)
      5) C7 -> D8 (-1420)
      6) F6 -> G5 (-1420)
      7) F6 -> G7 (-1420)
    > 2
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  w  .  .  .  
    D  .  .  .  b  .  .  .  .  
    C  b  .  .  .  .  .  b  .  
    B  .  .  .  .  .  .  .  b  
    A  .  .  W  .  W  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays E5 -> C3
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  b  .  w  .  .  .  b  .  
    B  .  .  .  .  .  .  .  b  
    A  .  .  W  .  W  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) C1 -> D2 (-1520)
      2) C7 -> D6 (-1520)
      3) C7 -> D8 (-1520)
      4) F6 -> G5 (-1520)
      5) F6 -> G7 (-1520)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  .  .  .  
    C  .  .  w  .  .  .  b  .  
    B  .  .  .  .  .  .  .  b  
    A  .  .  W  .  W  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays A5 -> B4
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  .  .  .  
    C  .  .  w  .  .  .  b  .  
    B  .  .  .  W  .  .  .  b  
    A  .  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) C7 -> D6 (-1520)
      2) C7 -> D8 (-1520)
      3) D2 -> E1 (-1520)
      4) D2 -> E3 (-1520)
      5) F6 -> G5 (-1520)
      6) F6 -> G7 (-1520)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  b  .  .  
    C  .  .  w  .  .  .  .  .  
    B  .  .  .  W  .  .  .  b  
    A  .  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays B4 -> C5
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  b  .  .  
    C  .  .  w  .  W  .  .  .  
    B  .  .  .  .  .  .  .  b  
    A  .  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) B8 -> C7 (-1820)
      2) D2 -> E1 (-1820)
      3) D2 -> E3 (-1820)
      4) D6 -> E5 (-1720)
      5) D6 -> E7 (-1720)
      6) F6 -> G5 (-1620)
      7) F6 -> G7 (-1620)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  b  .  .  
    C  .  .  w  .  W  .  b  .  
    B  .  .  .  .  .  .  .  .  
    A  .  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays C5 -> E7 -> G5
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  W  .  .  .  
    F  .  .  .  .  .  .  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  .  .  .  
    C  .  .  w  .  .  .  b  .  
    B  .  .  .  .  .  .  .  .  
    A  .  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) C7 -> D6 (-1920)
      2) C7 -> D8 (-1920)
      3) D2 -> E1 (-1820)
      4) D2 -> E3 (-1820)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  W  .  .  .  
    F  .  .  .  .  .  .  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  b  .  .  
    C  .  .  w  .  .  .  .  .  
    B  .  .  .  .  .  .  .  .  
    A  .  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays C3 -> B2
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  W  .  .  .  
    F  .  .  .  .  .  .  .  .  
    E  .  .  .  .  .  .  .  .  
    D  .  b  .  .  .  b  .  .  
    C  .  .  .  .  .  .  .  .  
    B  .  w  .  .  .  .  .  .  
    A  .  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) D2 -> E1 (-1920)
      2) D2 -> E3 (-1920)
      3) D6 -> E5 (-1920)
      4) D6 -> E7 (-1920)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  W  .  .  .  
    F  .  .  .  .  .  .  .  .  
    E  b  .  .  .  .  .  .  .  
    D  .  .  .  .  .  b  .  .  
    C  .  .  .  .  .  .  .  .  
    B  .  w  .  .  .  .  .  .  
    A  .  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays B2 -> A1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  W  .  .  .  
    F  .  .  .  .  .  .  .  .  
    E  b  .  .  .  .  .  .  .  
    D  .  .  .  .  .  b  .  .  
    C  .  .  .  .  .  .  .  .  
    B  .  .  .  .  .  .  .  .  
    A  W  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) D6 -> E5 (-4294967296)
      2) D6 -> E7 (-4294967296)
      3) E1 -> F2 (-4294967296)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  W  .  .  .  
    F  .  .  .  .  .  .  .  .  
    E  b  .  .  .  b  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  .  .  .  .  .  .  .  .  
    B  .  .  .  .  .  .  .  .  
    A  W  .  W  .  .  .  W  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays A7 -> B6
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  W  .  .  .  
    F  .  .  .  .  .  .  .  .  
    E  b  .  .  .  b  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  .  .  .  .  .  .  .  .  
    B  .  .  .  .  .  W  .  .  
    A  W  .  W  .  .  .  .  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) E1 -> F2 (-4294967296)
      2) E5 -> F4 (-4294967296)
      3) E5 -> F6 (-4294967296)
    > 3
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  W  .  .  .  
    F  .  .  .  .  .  b  .  .  
    E  b  .  .  .  .  .  .  .  
    D  .  .  .  .  .  .  .  .  
    C  .  .  .  .  .  .  .  .  
    B  .  .  .  .  .  W  .  .  
    A  W  .  W  .  .  .  .  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays G5 -> E7
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  .  .  .  .  .  .  .  
    E  b  .  .  .  .  .  W  .  
    D  .  .  .  .  .  .  .  .  
    C  .  .  .  .  .  .  .  .  
    B  .  .  .  .  .  W  .  .  
    A  W  .  W  .  .  .  .  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
      1) E1 -> F2 (-4294967296)
    > 1
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  w  .  .  .  .  .  .  .  
    F  .  b  .  .  .  .  .  .  
    E  .  .  .  .  .  .  W  .  
    D  .  .  .  .  .  .  .  .  
    C  .  .  .  .  .  .  .  .  
    B  .  .  .  .  .  W  .  .  
    A  W  .  W  .  .  .  .  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    White's move
    
    Minimax plays G1 -> E3
    
    
    
               White
    
    H  .  w  .  w  .  w  .  w  
    G  .  .  .  .  .  .  .  .  
    F  .  .  .  .  .  .  .  .  
    E  .  .  w  .  .  .  W  .  
    D  .  .  .  .  .  .  .  .  
    C  .  .  .  .  .  .  .  .  
    B  .  .  .  .  .  W  .  .  
    A  W  .  W  .  .  .  .  .  
       1  2  3  4  5  6  7  8
    
               Black
    
    Black's move
    
    Possible moves:
  
  _White has one at this point_

