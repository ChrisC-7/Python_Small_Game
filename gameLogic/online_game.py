# online_game.py
from gameLogic.board import Board
from gameLogic.player import Player, AIPlayer
from gameLogic.rule import TicTacToeRule
from gameLogic.game_base import GameBase
from gameLogic.engine import GameEngine
from utils.log_utils import GameLogger
from typing import List

class OnlineGame():

    def __init__(self, mode = "tictatoe"):
        if mode == "tictatoe":
            self.engine = GameEngine(3, 3)
        else: 
            self.engine = GameEngine(15, 5)
        self.players = []
        self.logger = GameLogger()
        self.engine.logger = self.logger

    def set_players(self, player_list: List[Player]):
        self._players = player_list
        self.engine.players = player_list

    def current_player_id(self):
        return self.engine.current_player().id
        
    def is_player_turn(self, player_id: int) -> bool: 
        return self.current_player_id() == player_id

    def place_and_check(self, player_id: int, x: int, y: int) ->str:
        if not self.is_player_turn(player_id):
            return "not_your_turn"
        result = self.engine.place_piece(x, y)
        return result if result else "invalid"
    
    def get_winner(self) -> int:
        return self.engine.current_player().id
    
    def get_board_str(self) -> str:
        return str(self.engine.board)
    
    def restart(self):
        self.engine.restart_game()

