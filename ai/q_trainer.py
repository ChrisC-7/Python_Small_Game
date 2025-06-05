from gameLogic.player import QLearningAIPlayer, AIPlayer
from gameLogic.board import Board
from gameLogic.rule import TicTacToeRule
from ai.ai_strategy import QLearningStrategy
import random
import json
import os

SAVE_PATH = "q_model.json"
NUM_EPISODES = 100000 
SAVE_EVERY = 10000
WIN_CONDITION = 5
BOARD_SIZE = 15

def create_players():
    s1 = QLearningStrategy()
    p1 = AIPlayer(0, "QL-1", "X", s1)
    p2 = AIPlayer(1, "QL-2", "O", s1)
    p1.set_opponent(p2)
    p2.set_opponent(p1)
    return p1, p2, s1


def run_episode(p1, p2):
    board = Board(BOARD_SIZE)
    rule = TicTacToeRule(board, WIN_CONDITION)
    players = [p1, p2]
    turn = 0
    move_trace = []
    
    while True:
        player = players[turn]
        board_state = board.get_state()
        move = player.get_move(board_state)
        x, y = move[0] - 1, move[1] - 1

        if not board.check_available(x, y):
            continue

        board.set_piece(x, y, player.symbol)
        move_trace.append((board_state, move, player))

        if rule.is_win(player, move[0], move[1]):
            # win rewards 1, lose -1
            for b, m, pl in move_trace:
                reward = 1.0 if pl == player else -1.0
                pl.observe(b, m, reward, board.get_state())
            # return player.id
            return turn

        if board.check_full():
            for b, m, pl in move_trace:
                pl.observe(b, m, 0.0, board.get_state())
            return None

        turn = (turn + 1) % 2

def save_q_table(player: QLearningAIPlayer):
    q_table_serializable = {
        state: {f"{a[0]},{a[1]}": value for a, value in actions.items()}
        for state, actions in player.q_table.items()
    }

    with open(SAVE_PATH, "w") as f:
        json.dump(q_table_serializable, f)
    print(f"Q-table saved to {SAVE_PATH}")


def train():
    p1, p2 = create_players()
    results = {"p1": 0, "p2": 0, "draw": 0}

    for episode in range(1, NUM_EPISODES + 1):
        # winner = vs_random(p1, p2)
        winner = run_episode(p1, p2)
        if winner == 0:
            results["p1"] += 1
        elif winner == 1:
            results["p2"] += 1
        else:
            results["draw"] += 1

        if episode % SAVE_EVERY == 0:
            save_q_table(p1)
            print(f"Episode {episode} - P1 Win: {results['p1']} | P2 Win: {results['p2']} | Draw: {results['draw']}")
            results = {"p1": 0, "p2": 0, "draw": 0}

if __name__ == "__main__":
    train()
