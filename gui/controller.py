# gui/controller.py

# import sys
# sys.path.append('..')
from gameLogic.board import Board
from gameLogic.rule import TicTacToeRule
from gameLogic.player import Human_Player, AIPlayer, QLearningAIPlayer
from gui.events import events

class GameController:
    def __init__(self):
        self.board = Board(15)
        self.rule = TicTacToeRule(self.board, 5)
        self.players = [ Human_Player(0, "Player1", "X"),
                         AIPlayer(1, "AI", "O")]
        self.turn = 0
        self.finished = False
        events.on("board_click", self.handle_click)
        events.on("restart", self.restart)

    def handle_click(self, row, col):
        if self.finished or isinstance(self.players[self.turn], AIPlayer):
            return
        self.make_move(row, col)

    def make_move(self, row, col):
        player = self.players[self.turn]
        if self.board.check_available(row, col):
            self.board.set_piece(row, col, player.symbol)
            events.emit("piece_placed", row, col, player.symbol)

            if self.rule.is_win(player, row + 1, col + 1):
                self.finished = True
                events.emit("game_over", f"{player.name} wins!")
            elif self.board.check_full():
                self.finished = True
                events.emit("game_over", "It's a draw!")
            else:
                self.turn = (self.turn + 1) % 2
                if isinstance(self.players[self.turn], AIPlayer):
                    events.emit("ai_turn", self.players[self.turn])

    def ai_move(self):
        ai = self.players[self.turn]
        x, y = ai.get_move(self.board.get_state())
        self.make_move(x - 1, y - 1)

    def restart(self):
        self.board.create_board()
        self.rule = TicTacToeRule(self.board, 5)
        self.turn = 0
        self.finished = False
        events.emit("game_over", "New game started!") 