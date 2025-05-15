##
#  This module defines a class that models a player class 
#
from Board import Board 
class Player:
   
   def __init__(self, playOrder = 1, name = "A", symbol = 'x' ):
      self._playOrder = playOrder
      self._name = name
      self._symbol = symbol
      self._isAI = False

   @property
   def symbol(self):
      return self._symbol


   
class AIPlayer(Player):
   def __init__(self, playOrder=1, name="A", symbol='x'):
      super().__init__(playOrder, name, symbol)
      self._isAI = True



   
