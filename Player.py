##
#  This module defines a class that models a player class 
#

class Player:
   
   def __init__(self, playOrder = 1, symbol = 'x' ):
      self._playOrder = playOrder
      self._symbol = symbol
