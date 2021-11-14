import { useState } from "react";
import "./ConnectX.css";
import { Button } from "react-bootstrap";
import { ConnectXImpl, NONE, WHITE_PLAYER } from "./ConnectXImpl";
import { MinimaxPlayer } from "./MinimaxPlayer";
import { Link } from "react-router-dom";

export interface Player {
  disableMove: boolean;
  automated: boolean;
  onMoveReady: (move: number, game: ConnectXImpl) => number;
  inDecision: boolean;
}

class ManualPlayer implements Player {
  disableMove = false;
  onMoveReady: (move: number, game: ConnectXImpl) => number;
  automated = false;
  inDecision = false;

  constructor(onMoveReady: (move: number, game: ConnectXImpl) => number) {
    this.onMoveReady = onMoveReady;
  }
}

export interface GameOptionsProps {
  game: ConnectXImpl;
  setGame: (g: ConnectXImpl) => void;
  updatePage: () => void;
  setPlayer: (isManual: boolean, whichPlayer: number) => void;
  players: Player[];
}
function GameOptions(props: GameOptionsProps) {
  const { game, setGame, updatePage, setPlayer, players } = props;

  const playerStr = (player: Player) => {
    return player.automated ? "Auto" : "Manual";
  };

  return (
    <>
      <section id="game-options">
        <h3>Game Options</h3>
        <Button onClick={() => { game.resetGame(); updatePage(); }}>
          New Game
        </Button>
        <Button onClick={() => setPlayer(players[0].automated, 0)}>
          Player 1: {playerStr(players[0])}
        </Button>
        <Button onClick={() => setPlayer(players[1].automated, 1)}>
          Player 2: {playerStr(players[1])}
        </Button>
        <Button onClick={() => { game.undoLastMove(); updatePage(); }}>
          Undo last move
        </Button>
        <section style={{marginTop:"2vh",fontSize:"1.5em"}}>
          BLACK = B<br/>
          WHITE = W<br/>
          NONE  = .
        </section>
      </section>
    </>
  );
}

export interface GameSettingsProps {
  game: ConnectXImpl;
  setGame: (g: ConnectXImpl) => void;
  updatePage: () => void;
}
function GameSettings(props: GameSettingsProps) {
  const { game, setGame, updatePage } = props;

  const generateSetConditionWrapper = (doGameSet: () => ConnectXImpl) => {
    let allowReset = true;
    if (game.moveHistory.length > 0) {
      allowReset = confirm("Doing this will reset the game. Do you want to continue?");
    }
    if (allowReset) {
      setGame(doGameSet());
    }
  };

  const setCondition = (name: string, maxAllowed: number, minAllowed: number, setter: (n: number) => ConnectXImpl) => {
    const colStr = (document.getElementById(name) as HTMLInputElement).value;
    const col = +colStr;
    if (col < minAllowed || col > maxAllowed) {
      alert("Columns must be between 1 and 7");
      return -1;
    }

    generateSetConditionWrapper(() => setter(col));
  };

  return (
    <section id="game-settings">
      <h3>Game Conditions</h3>
      <div>
        {`(${game.cols})`} &nbsp;
        <input placeholder="Enter columns" id="cols" type="number" />
        <Button type="button" onClick={() => setCondition("cols", 7, 1, (n) => new ConnectXImpl(n, game.rows, game.win))}>
          Set
        </Button>
      </div>
      <div>
        {`(${game.rows})`} &nbsp;
        <input placeholder="Enter rows" id="rows" type="number" />
        <Button type="button" onClick={() => setCondition("rows", 6, 1, (n) => new ConnectXImpl(game.cols, n, game.win))}>
          Set
        </Button>
      </div>
      <div>
        {`(${game.win})`} &nbsp;
        <input placeholder="Enter win condition" id="wins" type="number" />
        <Button type="button" onClick={() => setCondition("wins", 7, 1, (n) => new ConnectXImpl(game.cols, game.rows, n))}>
          Set
        </Button>
      </div>
    </section>
  );
}

export interface ConnectXProps {
  rows?: number;
  cols?: number;
  requiredToWin?: number;
  defaultAutoDelay?: number;
}

function getManualPlayerMove(): number {
  const col = (document.getElementById("move") as HTMLInputElement).value;
  if (!col) {
    alert(`Invalid column given: ${col}`);
    return -1;
  }

  return +col;
}

function setupManualPlayer(): ManualPlayer {
  const onMoveReady = (move: number, _: ConnectXImpl) => {
    return move;
  };

  const manualPlayer = new ManualPlayer(onMoveReady);
  return manualPlayer;
}

export function ConnectX(props: ConnectXProps) {
  const { rows, cols, requiredToWin } = props;
  const defaultAutoDelay = props.defaultAutoDelay || 2;
  console.log(defaultAutoDelay);

  const [connectXGame, setConnectXGame] = useState(
    new ConnectXImpl(cols, rows, requiredToWin)
  );
  const [players, setPlayers] = useState([setupManualPlayer(), setupManualPlayer()]);
  const [update, setUpdate] = useState(false);
  const [inDecision, setInDecision] = useState(false);
  const [d, sd] = useState(0);

  const onMoveMade = (col: number) => {
    connectXGame.insert(col);
    setUpdate(!update);
  };

  console.log("D IS", d);

  const setPlayerToSomething = (isManual: boolean, whichPlayer: number): void => {
    const newPlayerArr = [...players];
    const newPlayer = isManual ? setupManualPlayer() : new MinimaxPlayer();
    newPlayerArr[whichPlayer] = newPlayer;
    setPlayers(newPlayerArr);
  };

  const onMoveHistory = () => {
    const moveHistory = (document.getElementById("move-history") as HTMLInputElement).value.trim();
    if (moveHistory.length === 0) {
      setConnectXGame(ConnectXImpl.getGameFromHistory([]));
      return;
    }
    const moveHistoryL = moveHistory.split(" ").map(v => +v);
    const newConnectXGame = ConnectXImpl.getGameFromHistory(moveHistoryL);
    setConnectXGame(newConnectXGame);
  };

  // console.log(connectXGame.getBoardRepr());

  const whichPlayer: number = +(connectXGame.getWhoseMove() === WHITE_PLAYER);
  const currPlayer = players[whichPlayer];
  const doMoveDisabled = currPlayer.disableMove;

  const onManualMove = () => {
    if (!doMoveDisabled) {
      const moveMade = getManualPlayerMove();
      const actualMove = players[whichPlayer].onMoveReady(moveMade, connectXGame);
      onMoveMade(actualMove);
    } else {
      alert("Waiting for automated move!");
    }
  };

  if (currPlayer.automated && connectXGame.checkForWin() === NONE && connectXGame.getValidMoves().length > 0 && !inDecision) {
    sd(d + 1);
    console.log("INSIDE THIS LOOP!");
    console.log(connectXGame.copy().board);
    const nextMove = players[whichPlayer].onMoveReady(-1, connectXGame.copy());
    onMoveMade(nextMove);
  }

  return (
    <div className="page">
      <h2>Connect X Demo</h2>
      <aside>
        Please navigate to <Link to="/minimax_algorithm">our minimax tutorial</Link> for more information on minimax
      </aside>
      <main>
        <div id="board" dangerouslySetInnerHTML={{ __html: connectXGame.getBoardRepr().replaceAll("\n", "<br>").replaceAll(" ", "&nbsp;")}} />
        <section id="game-metadata">
          <p>Current move: {connectXGame.getWhoseMove()}</p>
          {connectXGame.gameOver ? (<p>Winner: {connectXGame.getWinningPlayer()}</p>) : null}
        </section>
        {connectXGame.gameOver ? null : (<section style={{marginTop:0}}>
          <input placeholder={`Enter column from 0-${connectXGame.cols - 1}`} id="move" type="number" />
          <Button type="button" onClick={onManualMove} disabled={doMoveDisabled}>
            Do move
          </Button>
        </section>)}
        <GameOptions
          game={connectXGame}
          setGame={setConnectXGame}
          updatePage={() => setUpdate(!update)}
          setPlayer={setPlayerToSomething}
          players={players}
        />
        <GameSettings
          game={connectXGame}
          setGame={setConnectXGame}
          updatePage={() => setUpdate(!update)}
        />
        <section>
          <h3>Advanced Options</h3>
          <input placeholder="Enter numbers as CSV" id="move-history" />
          <Button type="button" onClick={onMoveHistory}>
            Set Move History
          </Button>
        </section>
      </main>
    </div>
  );
}
