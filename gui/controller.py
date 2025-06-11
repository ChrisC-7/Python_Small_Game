# gui/controller.py

from gameLogic.board import Board
from gameLogic.rule import TicTacToeRule
from gameLogic.player import Human_Player, AIPlayer
from gameLogic.engine import GameEngine
from gui.events import events
from utils.events import GameEndEvent
from utils.event_scope import gui_dispatcher
from ai.ai_strategy import QLearningStrategy

class GameController:
    def __init__(self):
        # Create Players
        self.players = [
            Human_Player(0, "Player1", "X"),
           Human_Player(1, "Player2", "O")
        ]
        # self.players[1].strategy.load('ai/q_model.json') 
        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])

        # Create Engine
        self.engine = GameEngine(board_size=15, win_condition=5, players=self.players, dispatcher = gui_dispatcher)
        self.finished = False

        events.on("board_click", self.handle_click)
        events.on("restart", self.restart)

    def handle_click(self, row, col):
        if self.finished or isinstance(self.engine.current_player(), AIPlayer):
            return
        self.process_move(row, col)
        print(f"Handling click at ({row},{col}), current player: {self.engine.current_player().name}")


    def process_move(self, row, col):
        event = self.engine.place_piece(row, col)  # 注意：引擎坐标是从1开始的
        if isinstance(event, GameEndEvent):
            self.finished = True
        print(f"Placing piece at ({row}, {col})")

        

    def ai_move(self):
        player = self.engine.current_player()
        if isinstance(player, AIPlayer):
            row, col = player.get_move(self.engine.board.get_state())
            self.process_move(row, col)

    def restart(self):
        self.engine.restart_game()
        self.finished = False
        events.emit("game_over", "New game started!")






# # import sys
# # sys.path.append('..')
# from gameLogic.board import Board
# from gameLogic.rule import TicTacToeRule
# from gameLogic.player import Player, Human_Player, AIPlayer
# from gameLogic.engine import GameEngine
# from gui.events import events
# from typing import List

# class GameController:
#     def __init__(self):
#         p1 = Human_Player(0, "Player1", "X")
#         p2 = Human_Player(1, "Player2", "O")

#         p1.set_opponent(p2)
#         p2.set_opponent(p1)

#         self.engine = GameEngine(board_size = 15, win_condition = 5, players=[p1, p2] )
#         self.finished = False

#         events.on("board_click", self.handle_click)
#         events.on("restart", self.restart)

#     def handle_click(self, row, col):
#         if self.finished or isinstance(self.engine.current_player(), AIPlayer):
#             return
#         self.make_move(row, col)

#     def make_move(self, row, col):
#         # player = self.players[self.turn]
#         event = self.engine.place_piece(row, col)

#         if self.board.check_available(row, col):
#             self.board.set_piece(row, col, player.symbol)
#             events.emit("piece_placed", row, col, player.symbol)

#             if self.rule.is_win(player, row + 1, col + 1):
#                 self.finished = True
#                 events.emit("game_over", f"{player.name} wins!")
#             elif self.board.check_full():
#                 self.finished = True
#                 events.emit("game_over", "It's a draw!")
#             else:
#                 self.turn = (self.turn + 1) % 2
#                 if isinstance(self.players[self.turn], AIPlayer):
#                     events.emit("ai_turn", self.players[self.turn])

#     def ai_move(self):
#         ai = self.players[self.turn]
#         x, y = ai.get_move(self.board.get_state())
#         self.make_move(x - 1, y - 1)

#     def restart(self):
#         self.board.create_board()
#         self.rule = TicTacToeRule(self.board, 5)
#         self.turn = 0
#         self.finished = False
#         events.emit("game_over", "New game started!") 