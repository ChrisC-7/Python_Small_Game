##
#  This module defines a class that models a player class 
#
import board
class Player:
   
   def __init__(self, playOrder = 1, name = "A", symbol = 'x' ):
      self._playOrder = playOrder
      self._name = name
      self._symbol = symbol
      self._isAI = False
      self._isWin = False

   @property
   def symbol(self) -> str:
      return self._symbol
   
   @property
   def name(self) -> str:
      return self._name
   
   def mark_as_winner(self):
      self._isWin = True
   
   def isWin(self):
      return self._isWin
   
class AIPlayer(Player):
   def __init__(self, playOrder=1, name="A", symbol='x'):
      super().__init__(playOrder, name, symbol)
      self._isAI = True



   
