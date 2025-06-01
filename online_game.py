# online_game.py
import board
import player
from Rule import TicTacToeRule
from game_base import GameBase
from typing import List

class OnlineGame(GameBase):

    def __init__(self, win_condition=3):
        self._board = board.Board()
        self._players = []
        self._win_condition = win_condition
        self._rule = TicTacToeRule(self._board, self._win_condition)

    def set_players(self, player_list: List[player.Human_Player]):
        self._players = player_list

    def place_piece(self, player_id: int, x: int, y: int) -> bool:
        return self._board.place_piece(x - 1, y - 1, self._players[player_id].symbol)

    @property
    def board(self):
        return self._board

    def check_win(self, player_id: int, x: int, y: int) -> bool:
        return self._rule.is_win(self._players[player_id], x, y)

    def check_draw(self) -> bool:
        return self._rule.is_draw()
    
    def restart_game(self):
        self._board.create_board()
        
