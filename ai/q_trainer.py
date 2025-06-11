# q_trainer.py
import os
import json
import random
from gameLogic.player import AIPlayer
from gameLogic.board import Board
from gameLogic.rule import TicTacToeRule
from ai.ai_strategy import QLearningStrategy

SAVE_PATH = os.path.join("ai", "q_model.json")
NUM_EPISODES = 100000
SAVE_EVERY = 10000
WIN_CONDITION = 5
BOARD_SIZE = 8

def create_players():
    s1 = QLearningStrategy()
    s2 = QLearningStrategy()
    p1 = AIPlayer(0, "QL-1", "X", s1)
    p2 = AIPlayer(1, "QL-2", "O", s2)
    p1.set_opponent(p2)
    p2.set_opponent(p1)
    return p1, p2

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
            total_steps = len(move_trace)
            for i, (b, m, pl) in enumerate(move_trace):
                reward = (1.0 + (total_steps - i) * 0.01) if pl == player else (-1.0 - i * 0.01)
                pl.observe(b, m, reward, board.get_state())
            return turn

        if board.check_full():
            for b, m, pl in move_trace:
                pl.observe(b, m, 0.0, board.get_state())
            return None

        turn = (turn + 1) % 2

def train():
    p1, p2 = create_players()
    results = {"p1": 0, "p2": 0, "draw": 0}

    for episode in range(1, NUM_EPISODES + 1):
        winner = run_episode(p1, p2)
        if winner == 0:
            results["p1"] += 1
        elif winner == 1:
            results["p2"] += 1
        else:
            results["draw"] += 1

        if episode % SAVE_EVERY == 0:
            p1.save_model(SAVE_PATH)
            print(f"Episode {episode} - P1 Win: {results['p1']} | P2 Win: {results['p2']} | Draw: {results['draw']}")
            results = {"p1": 0, "p2": 0, "draw": 0}

if __name__ == "__main__":
    train()
