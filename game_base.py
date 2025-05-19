# game_base.py
from abc import ABC, abstractmethod
from typing import Tuple, List
import Player

class GameBase(ABC):

    @abstractmethod
    def place_piece(self, player_id: int, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def get_board_state(self) -> List[List[str]]:
        pass

    @abstractmethod
    def check_win(self, player_id: int, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def check_draw(self) -> bool:
        pass

    
