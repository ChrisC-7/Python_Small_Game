##
#  This module defines a class that models a player class 
#
import board
from abc import ABC, abstractmethod 
import random
from typing import List, Tuple
import json

class Player(ABC):
   def __init__(self, id = 1, name = "A", symbol = 'x' ):
      self._id = id
      self._name = name
      self._symbol = symbol
      self._isWin = False

   @property
   def id(self):
      return self._id
   
   @property
   def name(self): 
      return self._name
   
   @property
   def symbol(self):
      return self._symbol
   
   @property
   def is_win(self):
      return self._isWin
   
   def mark_as_winner(self):
      self._isWin = True

   @abstractmethod
   def get_move(self, board_state):
      pass

   def load_q_table(self, path):
      pass

class Human_Player(Player):
   def get_move(self, board_state):
      x = int(input("Enter row (x): "))
      y = int(input("Enter col (y): "))
      return x, y

   
class AIPlayer(Player):
   def get_move(self, board_state):
      size = len(board_state)
      available = [(i + 1, j + 1) for i in range(size) for j in range(size) if board_state[i][j] == ' ']
      return random.choice(available) if available else (1, 1)
   
   def observe(self, board_state, action, reward, next_state):
        pass


class QLearningAIPlayer(AIPlayer):

   def __init__(self, id=1, name="QL", symbol='x' , alpha=0.1, gamma=0.9, epsilon=0.1):
      super().__init__(id, name, symbol)
      self.q_table = {}
      self.alpha = alpha
      self.gamma = gamma
      self.epsilon = epsilon



   def observe(self, board_state : List[List[str]], action: tuple, reward: float, next_state: List[List[str]] ):
      state_key = self.encode_board(board_state)
      next_key = self.encode_board(next_state)

      self.q_table.setdefault(state_key, {})
      self.q_table[state_key].setdefault(action, 0.0)

      next_max = max(self.q_table.get(next_key, {}).values(), default=0.0)

      old_value = self.q_table[state_key][action]
      new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
      self.q_table[state_key][action] = new_value


   def encode_board(self, board_state: List[List[str]]) -> str:
      return ''.join(''.join(row) for row in board_state)
   
   def get_move(self, board_state)-> Tuple[int, int]:
    state_key = self.encode_board(board_state)
    size = len(board_state)
    available_moves = [(i + 1, j + 1) for i in range(size) for j in range(size) if board_state[i][j] == ' ']

    # 探索
    if random.random() < self.epsilon:
        return random.choice(available_moves)

    # 利用
    q_values = self.q_table.get(state_key, {})
    best_move = None
    best_score = float('-inf')

    for move in available_moves:
        score = q_values.get(move, 0.0)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move if best_move else random.choice(available_moves)

   def load_q_table(self, path):
      with open(path, "r") as f :
         raw_table = json.load(f)

      self.q_table = {
         state: {
               tuple(map(int, k.split(","))) : v
               for k, v in action_dict.items()
          }
          for state, action_dict in raw_table.items()
      } 