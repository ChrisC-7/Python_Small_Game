# local_game.py
import board
import player
from Rule import TicTacToeRule
from game_base import GameBase
from log_utils import GameLogger


class LocalGame(GameBase):

    def __init__(self, mode = "tictatoe"):
        if mode == "tictatoe":
            self._board = board.Board(3)
            self._win_condition = 3
        if mode == "gomoku":
            self._board = board.Board(15)
            self._win_condition = 5
        self._players : list[player.Human_Player] = []
        self._rule = TicTacToeRule(self._board, self._win_condition)
        self.init_players()
        self._logger = GameLogger()

    def init_players(self):
        for i in range(2):
            name = input(f"Enter Player {i + 1} name: ")
            symbol = input(f"Enter Player {i + 1} symbol: ")
            is_ai = input(f"Is Player {i + 1} an AI player? (y/n): ").lower()=='y'
            if is_ai:
                self._players.append(player.AIPlayer(i, name, symbol))
            else:
                self._players.append(player.Human_Player(i, name, symbol))

    def place_piece(self, player_id: int, x: int, y: int) -> bool:
        return self._board.place_piece(x - 1, y - 1, self._players[player_id].symbol)

    def get_board_state(self):
        return self._board.get_state()

    def check_win(self, player_id: int, x: int, y: int) -> bool:
        return self._rule.is_win(self._players[player_id], x, y)

    def check_draw(self) -> bool:
        return self._rule.is_draw()

    def play(self):
        turn = 0
        while True:
            player = self._players[turn] 
            print(f"Player {player.name}'s turn")
            x, y = player.get_move(self._board.get_state())
            print(f"{player.name} chooses ({x}, {y})")
            
            if self.place_piece(turn, x, y):
                print(self._board)
                self._logger.log_step(
                    player_id = player.id,
                    player_name = player.name,
                    symbol = player.symbol,
                    x = x, y = y,
                    board_state = self._board.get_state() 
                )
                if self.check_win(turn, x, y) or self.check_draw():
                    if self.check_win(turn, x, y):
                        print(f"{player.name} wins!")
                        self._logger.log_result("win")
                        self._logger.save_trace()
                    else:
                        print("It's a draw!")
                        self._logger.log_result("draw")
                        self._logger.save_trace()
                    choice = input("Play again? (y/n): ")
                    if choice.lower() == 'y':
                        self.restart_game()
                    else: break
                turn = (turn + 1) % 2
            else:
                print("Invalid move. Try again.")

    def restart_game(self):
        self._board.create_board()
        self._logger = GameLogger()

if __name__ == "__main__":
    g = LocalGame("gomoku")
    g.play()

