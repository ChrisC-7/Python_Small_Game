##
#  This module defines a class that models a player class 
#
# import board
from abc import ABC, abstractmethod 
import random
from typing import List, Tuple
from gameLogic.board import Board
from ai.ai_strategy import AIStrategy, RuleBasedStrategy
from copy import deepcopy
import json

class Player(ABC):
   def __init__(self, id = 1, name = "A", symbol = 'x' ):
      self._id = id
      self._name = name
      self._symbol = symbol
      self._isWin = False
      self._opponent = None

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
   def get_move(self, board_state:List[List[str]]) -> Tuple[int, int]:
      pass

   def load_q_table(self, path):
      pass

   def observe(self, board_state, action, reward, next_state):
        """Do nothing"""
        pass
   
   def set_opponent(self, opponent):
      self._opponent = opponent

class Human_Player(Player):
   def get_move(self, board_state):
      x = int(input("Enter row (x): "))
      y = int(input("Enter col (y): "))
      return x, y

   
class AIPlayer(Player):

   def __init__(self, id, name, symbol, strategy: AIStrategy = RuleBasedStrategy()):
      super().__init__(id, name, symbol)
      self.strategy = strategy

   def get_move(self, board_state):
      return self.strategy.select_move(board_state)
   
   def observe(self, board_state, action, reward, next_state):
      return self.strategy.observe(board_state, action, reward, next_state)
      
   def set_opponent(self, opponent: Player):
      super().set_opponent(opponent)
      self.strategy.set_symbols(self.symbol, opponent.symbol)   
   
   def load_model(self, path: str):
        if hasattr(self.strategy, "load"):
            self.strategy.load(path)

   def save_model(self, path: str):
        if hasattr(self.strategy, "save"):
            self.strategy.save(path)