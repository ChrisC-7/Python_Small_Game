# game_base.py
from abc import ABC, abstractmethod
from gameLogic.board import Board

class GameBase(ABC):

    @abstractmethod
    def place_piece(self, player_id: int, x: int, y: int) -> bool:
        pass

    @property
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

    
