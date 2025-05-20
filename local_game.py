# local_game.py
import board
import player
from Rule import TicTacToeRule
from game_base import GameBase

class LocalGame(GameBase):

    def __init__(self, win_condition=3):
        self._board = board.Board()
        self._players : list[player.Player] = []
        self._win_condition = win_condition
        self._rule = TicTacToeRule(self._board, self._win_condition)
        self.init_players()

    def init_players(self):
        for i in range(2):
            name = input(f"Enter Player {i + 1} name: ")
            symbol = input(f"Enter Player {i + 1} symbol: ")
            self._players.append(player.Player(i, name, symbol))

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
            x = int(input("Enter row (x): "))
            y = int(input("Enter col (y): "))
            if self.place_piece(turn, x, y):
                self._board.print_board()
                if self.check_win(turn, x, y) or self.check_draw():
                    if self.check_win(turn, x, y):
                        print(f"{player.name} wins!")
                    else:
                        print("It's a draw!")
                    choice = input("Play again? (y/n): ")
                    if choice.lower() == 'y':
                        self.restart_game()
                    else: break
                turn = (turn + 1) % 2
            else:
                print("Invalid move. Try again.")

    def restart_game(self):
        self._board.create_board()

if __name__ == "__main__":
    g = LocalGame()
    g.play()

