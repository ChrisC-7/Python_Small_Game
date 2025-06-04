from gameLogic.board import Board
from gameLogic.rule import TicTacToeRule
from gameLogic.player import Player, Human_Player, AIPlayer, QLearningAIPlayer
from utils.log_utils import GameLogger
from gameLogic.game_base import GameBase
from typing import List

class GameEngine(GameBase):
    def __init__(self, board_size = 3, win_condition = 3, players = None, logger = None):
        self._board = Board(board_size)
        self.rule = TicTacToeRule(self.board, win_condition)
        self.players:List[Player] = players or []
        self.logger:GameLogger = logger
        self.turn = 0
        self.finished = False

    def place_piece(self, x, y):
        player = self.players[self.turn]
        if not self.board.check_available(x-1, y-1) or self.finished:
            return False
        
        self.board.set_piece(x-1, y-1, player.symbol)
        if self.logger:
            self.logger.log_step(player.name, player.id, player.symbol, x, y, self.board.get_state())
        if self.check_win(self.turn, x, y):
            return "win"
        elif self.check_draw():
            return "draw"
        else:
            self.turn = (self.turn + 1) % 2
            return "continue"    

    def current_player(self):
        return self.players[self.turn]

    @property
    def board(self) -> Board:
        return self._board
    
    def check_win(self, player_id, x, y):
        win = self.rule.is_win(self.players[player_id], x, y)
        if win and self.logger:            
            self.finished = True
            self.logger.log_result("win")
            self.logger.save_trace()
        return win
    
    def check_draw(self):
        draw = self.rule.is_draw()
        if draw and self.logger:
            self.finished = True
            self.logger.log_result("draw")
            self.logger.save_trace()
        return draw
    
    def restart_game(self):
        self.board.create_board()
        self.finished = False
        self.turn = 0
        if self.logger:
            self.logger = GameLogger()