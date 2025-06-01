##
#  This module defines a class that models a player class 
#
import board
from abc import ABC, abstractmethod 
import random
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

   
