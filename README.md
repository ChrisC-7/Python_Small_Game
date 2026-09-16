# Python Small Game — Networked Multiplayer Board Game System

A modular Python board-game system with a reusable game engine, TCP multiplayer networking, a framed JSON protocol, local/GUI front ends, game logging, and experimental AI agents.

This project started as a small Tic-Tac-Toe game and evolved into a broader game-system experiment. In networked mode, two clients connect to a server-authoritative game session, submit moves over TCP, and receive synchronized board updates and game results.

> An earlier version of this project previously ran on an Azure-hosted server. The exact Azure service or VM configuration is not preserved in this repository, so no more specific infrastructure claim is made here.

## Features

* Two-player multiplayer over TCP sockets
* Server-authoritative game state and turn management
* Length-prefixed JSON application protocol
* Reusable game engine with configurable board size and win condition
* Tic-Tac-Toe and Gomoku-style game configurations
* CLI and Tkinter GUI interfaces
* Game trace logging to JSON
* Pluggable AI strategies:

  * Random
  * Rule-based
  * Experimental tabular Q-learning

## Architecture

```text
Client 1                    Client 2
   │                           │
   │      TCP + framed JSON    │
   └───────────┐   ┌───────────┘
               ▼   ▼
        ┌───────────────┐
        │ Network Server│
        └───────┬───────┘
                │
                ▼
        ┌──────────────────┐
        │ OnlineGameSession│
        │ connections      │
        │ turns            │
        │ broadcasts       │
        └────────┬─────────┘
                 │
                 ▼
          ┌────────────┐
          │ GameEngine │
          └─────┬──────┘
                │
        ┌───────┴────────┐
        ▼                ▼
     Board             Rules
        │                │
        └───────┬────────┘
                ▼
           Game Events
                │
          ┌─────┴─────┐
          ▼           ▼
       Logging      UI / CLI
```

The project separates the main responsibilities into several modules:

| Module       | Responsibility                                                   |
| ------------ | ---------------------------------------------------------------- |
| `gameLogic/` | Board state, rules, players, turns, win/draw detection           |
| `network/`   | TCP sockets, protocol framing, connections, multiplayer sessions |
| `ai/`        | AI strategy interface and experimental agents                    |
| `gui/`       | Tkinter user interface and controller                            |
| `utils/`     | Events, dispatching, and game logging                            |

## Network Protocol

TCP provides a byte stream rather than application-level message boundaries, so each message is explicitly framed as:

```text
[4-byte big-endian payload length][UTF-8 JSON payload]
```

Example payload:

```json
{
  "action": "move",
  "data": {
    "x": 1,
    "y": 2
  }
}
```

`network/protocol.py` uses `recv_exact()` to read the full header and payload instead of assuming one call to `recv()` contains one complete application message.

### Current message types

| Direction        | Action          | Purpose                     |
| ---------------- | --------------- | --------------------------- |
| Client → Server  | `intro`         | Send player name and symbol |
| Server → Client  | `player id`     | Assign a player ID          |
| Server → Client  | `your_turn`     | Request a move              |
| Server → Client  | `your_turn(re)` | Retry after an invalid move |
| Server → Client  | `wait`          | Tell the opponent to wait   |
| Client → Server  | `move`          | Submit board coordinates    |
| Server → Clients | `update`        | Broadcast the updated board |
| Server → Clients | `result`        | Report win or draw          |
| Client → Server  | `restart`       | Vote to restart the game    |

## Project Structure

```text
.
├── ai/
│   ├── ai_strategy.py
│   ├── q_trainer.py
│   └── game_train.py
│
├── gameLogic/
│   ├── board.py
│   ├── engine.py
│   ├── game_base.py
│   ├── local_game.py
│   ├── online_game.py
│   ├── player.py
│   └── rule.py
│
├── gui/
│   ├── app.py
│   ├── board_canvas.py
│   ├── components.py
│   ├── controller.py
│   └── events.py
│
├── network/
│   ├── client.py
│   ├── common.py
│   ├── protocol.py
│   ├── server.py
│   └── session.py
│
├── utils/
│   ├── dispatcher.py
│   ├── event_scope.py
│   ├── events.py
│   └── log_utils.py
│
├── sever.py
├── requirements.txt
└── README.md
```

`sever.py` is an older server implementation and is currently retained as legacy code. The newer networking path lives under `network/`.

## Local Setup

Clone the repository:

```bash
git clone https://github.com/ChrisC-7/Python_Small_Game.git
cd Python_Small_Game
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The GUI uses `tkinter`, which is included with many Python installations but may require an OS package on some Linux systems.

## Run the Multiplayer Version

The current development configuration uses:

```text
HOST = 127.0.0.1
PORT = 65432
```

Open three terminals from the repository root.

### 1. Start the server

```bash
python -m network.server
```

### 2. Start the first client

```bash
python -m network.client
```

### 3. Start the second client

```bash
python -m network.client
```

The clients provide a player name and symbol, then send moves when the server grants their turn.

## Local GUI

A separate Tkinter-based 15×15 five-in-a-row interface is included:

```bash
python -m gui.app
```

The GUI is currently a local front end and is not integrated with the network client.

## AI Agents

AI behavior is implemented through an `AIStrategy` abstraction.

### RandomStrategy

Selects a random available position.

### RuleBasedStrategy

Scores candidate cells based on offensive and defensive line lengths and selects among the highest-scoring positions.

### QLearningStrategy

Implements an experimental tabular Q-learning agent with:

* epsilon-greedy exploration
* learning-rate decay
* exploration decay
* discounted future reward
* JSON model persistence

`ai/q_trainer.py` contains a self-play training experiment using an 8×8 board and a five-in-a-row win condition.

The Q-learning implementation is still experimental. Its board-state encoding and model persistence paths need repair and validation before any AI-performance claims should be made.

## Logging

Game traces are generated by `GameLogger` under:

```text
logs/
```

These files are runtime artifacts and should not be committed to Git.

The existing `.gitignore` already ignores `logs` and its contents.

## Current Limitations / Roadmap

This is a historical project being cleaned up into a portfolio-quality engineering artifact. The highest-value next work is reliability and cleanup rather than adding new features.

* Fix the network client's `player_id` handling.
* Verify the complete server + two-client game flow.
* Repair restart/disconnect handling.
* Remove or migrate the legacy root-level `sever.py`.
* Repair and test Q-learning board-state encoding and persistence.
* Add protocol-framing tests.
* Add game-engine rule tests.
* Add multiplayer-session tests.
* Move host/port configuration outside source code for remote deployment.
* Improve socket shutdown and reconnect behavior.
* Remove obsolete commented-out implementations once behavior is covered by tests.
* Support multiple concurrent game sessions if multiplayer rooms are added later.

## Project Motivation

The project became an experiment in moving from a single-file Python game toward a small system with explicit boundaries between:

* game logic
* networking
* message protocols
* UI
* AI strategies
* events
* logging

The goal of the current cleanup is to make those engineering decisions visible and reproducible rather than adding unnecessary complexity.
