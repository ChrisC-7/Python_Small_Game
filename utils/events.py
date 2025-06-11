#utils/events.py

from gameLogic.player import Player
from gameLogic.board import Board
class GameEvent: 
    def name(self):
        return self.__init__.__name__
    pass

class GameEndEvent(GameEvent):
    pass
class MovePlacedEvent(GameEvent):
    def __init__(self, x: int, y: int, player:Player, board: Board):
        self.x = x
        self.y = y
        self.player: Player = player
        self.board = board
    
class GameWonEvent(GameEndEvent):
    def __init__ (self, winner):
        self.winner = winner
    
class GameDrawEvent(GameEndEvent):
    pass

class InvalidMoveEvent(GameEvent):
    pass