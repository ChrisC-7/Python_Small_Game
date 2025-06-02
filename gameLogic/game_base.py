# game_base.py
from abc import ABC, abstractmethod
from typing import Tuple, List
from gameLogic.board import Board
# import player

class GameBase(ABC):

    @abstractmethod
    def place_piece(self, player_id: int, x: int, y: int) -> bool:
        pass

    
    def board(self) -> Board:
        pass

    @abstractmethod
    def check_win(self, player_id: int, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def check_draw(self) -> bool:
        pass

    @abstractmethod
    def restart_game(self):
        pass

    
