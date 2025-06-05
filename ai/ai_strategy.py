from abc import ABC, abstractmethod
from typing import List, Tuple
from copy import deepcopy
from gameLogic.board import Board
import json
import random

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

        return my_score * 2 + opp_score * 3
    

class QLearningStrategy(AIStrategy):
    def __init__(self, q_table = None, alpha = 0.1, gamma = 0.9, epsilon = 0.1):
        super().__init__()
        self.q_table = q_table or {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

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

    def encode_board(self, board):
        return ''.join(''.join(row) for row in board)

    def load(self, path):
        with open(path, "r") as f:
            raw_table = json.load(f)
        self.q_table = {
            state: {
                tuple(map(int, k.split(","))) : v
                for k, v in move_dict.items()
            }
            for state, move_dict in raw_table.items()
        }
    
    def save(self, path):
        serializable = {
            state: {f"{x},{y}": v for (x, y), v in move_dict.items()}
            for state, move_dict in self.q_table.items()
        }
        with open(path, "w") as f:
            json.dump(serializable, f, indent=2)
    # def observe(): 

    # def save_model(): 

