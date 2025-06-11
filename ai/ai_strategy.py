from abc import ABC, abstractmethod
from typing import List, Tuple
from copy import deepcopy
from gameLogic.board import Board
import json
import random
import os

class AIStrategy(ABC):
    def __init__(self):
        self.my_symbol = None
        self.opponent = None
    
    def set_symbols(self, symbol, opponent):
        self.my_symbol = symbol
        self.opponent = opponent

    @abstractmethod
    def select_move(self, board_state: List[List[str]]) -> Tuple[int, int]:
        pass

    # def observe(self, board, action, reward, next_board): 
    #     pass
    


class RandomStrategy(AIStrategy):
    def __init__(self):
        super().__init__()
        self.last_move = None
        self.last_direction = None


    def select_move(self, board_state: List[List[str]]) -> Tuple[int, int]:
        size = len(board_state)
        available = [(i + 1, j + 1) for i in range(size) for j in range(size) if board_state[i][j] == ' ']
        return random.choice(available) if available else (1, 1)
    
class RuleBasedStrategy(AIStrategy):
    def select_move(self, board_state):
        size = len(board_state)
        scores = [[0 for _ in range(size)] for _ in range(size)]

        temp_board = Board(size)
        temp_board._board = deepcopy(board_state)

        # evaluate the score for the board
        for x in range(size):
            for y in range(size):
                if board_state[x][y] != ' ':
                    continue
                scores[x][y] = self.count_score(temp_board, x, y)
            
        max_score = max(max(row) for row in scores)
        best_moves = [(x, y) for x in range(size) for y in range(size) if scores[x][y] == max_score]
        
        move = random.choice(best_moves)
        return move[0] + 1, move[1] + 1
    
    def count_score(self, board: Board, x: int, y: int):
        
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        board._board[x][y] = self.my_symbol
        my_score = max(board.check_line(self.my_symbol, x, y, dx, dy) for dx, dy in directions)
        board._board[x][y] = ' '


        board._board[x][y] = self.opponent
        opp_score = max(board.check_line(self.opponent, x, y, dx, dy) for dx, dy in directions)
        board._board[x][y] = ' '

        return my_score * 2 + opp_score * 5
    

class QLearningStrategy(AIStrategy):
    def __init__(self, q_table=None, alpha=0.1, gamma=0.9, epsilon=1.0,
                 epsilon_min=0.05, epsilon_decay=0.995,
                 alpha_min=0.01, alpha_decay=0.995):
        super().__init__()
        self.q_table = q_table or {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.alpha_min = alpha_min
        self.alpha_decay = alpha_decay

    def select_move(self, board_state):
        key = self.encode_board(board_state)
        size = len(board_state)
        available = [(i+1, j+1) for i in range(size) for j in range(size) if board_state[i][j] == " " ] 

        if random.random() < self.epsilon:
            return random.choice(available)
        
        best_score = float("-inf")
        best_move = None
        for move in available:
            score = self.q_table.get(key, {}).get(move, 0.0)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move or random.choice(available)

    # def encode_board(self, board):
    #     return tuple(tuple(row) for row in board)

    # def load(self, path):
    #     print("load here")
    #     with open(path, "r") as f:
    #         raw_table = json.load(f)
    #     self.q_table = {
    #         state: {
    #             tuple(map(int, k.split(","))) : v
    #             for k, v in move_dict.items()
    #         }
    #         for state, move_dict in raw_table.items()
    #     }
    
    # def save(self, path):
    #     serializable = {
    #         state: {f"{x},{y}": v for (x, y), v in move_dict.items()}
    #         for state, move_dict in self.q_table.items()
    #     }
    #     with open(path, "w") as f:
    #         json.dump(serializable, f, indent=2)

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        serializable = {
            self.encode_board_str(state): {f"{x},{y}": v for (x, y), v in move_dict.items()}
            for state, move_dict in self.q_table.items()
        }
        with open(path, "w") as f:
            json.dump(serializable, f, indent=2)

    def encode_board_str(self, board):
        return '|'.join(''.join(row) for row in board)
    
    def observe(self, state, action, reward, next_state):
        s_key = self.encode_board(state)
        a_key = action
        next_s_key = self.encode_board(next_state)

        if s_key not in self.q_table:
            self.q_table[s_key] = {}
        if a_key not in self.q_table[s_key]:
            self.q_table[s_key][a_key] = 0.0

        next_q_values = self.q_table.get(next_s_key, {})
        max_next_q = max(next_q_values.values(), default=0.0)

        old_value = self.q_table[s_key][a_key]
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * max_next_q)
        self.q_table[s_key][a_key] = new_value

        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.alpha = max(self.alpha_min, self.alpha * self.alpha_decay)

    def decode_board_str(self, board_str):
        rows = board_str.split('|')
        return tuple(tuple(cell for cell in row) for row in rows)

    def load(self, path):
        with open(path, "r") as f:
            raw_table = json.load(f)
        self.q_table = {
            self.decode_board_str(state_str): {
                tuple(map(int, k.split(","))): v
                for k, v in move_dict.items()
            }
            for state_str, move_dict in raw_table.items()
        }

    # def load(self, path):
    #     with open(path, "r") as f:
    #         raw_table = json.load(f)
    #     self.q_table = {
    #         eval(state): {
    #             tuple(map(int, k.split(","))): v
    #             for k, v in move_dict.items()
    #         }
    #         for state, move_dict in raw_table.items()
    #     }
    # def save_model(): 

