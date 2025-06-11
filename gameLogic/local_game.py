# local_game.py
import gameLogic.board as board
from gameLogic.player import Player, Human_Player, AIPlayer
from gameLogic.rule import TicTacToeRule
from gameLogic.game_base import GameBase
from utils.log_utils import GameLogger
from gameLogic.engine import GameEngine
from utils.event_scope import cli_dispatcher
from utils.events import GameEndEvent, InvalidMoveEvent
from ai.ai_strategy import QLearningStrategy

class LocalGame():

    def __init__(self, mode = "tictatoe"):
        self._players : list[Human_Player] = []
        self.init_players()
        if mode == "tictatoe":
            self.engine = GameEngine(3, 3, self._players, GameLogger(), dispatcher=cli_dispatcher)
        if mode == "gomoku":
            self.engine = GameEngine(8, 5, self._players, GameLogger(), dispatcher=cli_dispatcher)
        
    def init_players(self):
        for i in range(2):
            name = input(f"Enter Player {i + 1} name: ")
            symbol = input(f"Enter Player {i + 1} symbol: ")
            is_ai = input(f"Is Player {i + 1} an AI player? (y/n): ").lower()=='y'
            if is_ai:
                strategy = QLearningStrategy()
                print("success")
                strategy.load('ai/q_model.json') 
                
                player = AIPlayer(i, name, symbol, strategy)
                self._players.append(player)
                print(f"[DEBUG] Q-table loaded with {len(player.strategy.q_table)} board states.")
            else:
                self._players.append(Human_Player(i, name, symbol))

    # def place_piece(self, player_id: int, x: int, y: int) -> bool:
    #     return self._board.place_piece(x - 1, y - 1, self._players[player_id].symbol)

    # def get_board_state(self):
    #     return self._board.get_state()

    # def check_win(self, player_id: int, x: int, y: int) -> bool:
    #     return self._rule.is_win(self._players[player_id], x, y)

    # def check_draw(self) -> bool:
    #     return self._rule.is_draw()

    def play(self):
        while True:
            player = self.engine.current_player()
            print(f"It's player {player.name}'s turn now.")
            x, y = player.get_move(self.engine.board.get_state())
            event = self.engine.place_piece(x, y)

            while isinstance(event, InvalidMoveEvent):
                print("Invalid placement, Try again.")
                x, y = player.get_move(self.engine.board.get_state)
                event = self.engine.place_piece(x, y)


            # print(f"{player.name} chooses ({x}, {y})")
            print(self.engine.board)  # show current board
            cli_dispatcher.handle(event)

            # if  result == "win":
            #     print(f"{player.name} wins!")
            # elif result == "draw":
            #     print("It's a draw!")
            # else: continue

            if isinstance(event, GameEndEvent):
                choice = input("Play again? (y/n)")
                if choice.lower() == "y":
                    self.engine.restart_game()
                else:
                    break
        # turn = 0
        # while True:
        #     player = self._players[turn] 
        #     print(f"Player {player.name}'s turn")
        #     x, y = player.get_move(self._board.get_state())
        #     print(f"{player.name} chooses ({x}, {y})")
            
        #     if self.place_piece(turn, x, y):
        #         print(self._board)
        #         self._logger.log_step(
        #             player_id = player.id,
        #             player_name = player.name,
        #             symbol = player.symbol,
        #             x = x, y = y,
        #             board_state = self._board.get_state() 
        #         )
        #         if self.check_win(turn, x, y) or self.check_draw():
        #             if self.check_win(turn, x, y):
        #                 print(f"{player.name} wins!")
        #                 self._logger.log_result("win")
        #                 self._logger.save_trace()
        #             else:
        #                 print("It's a draw!")
        #                 self._logger.log_result("draw")
        #                 self._logger.save_trace()
        #             choice = input("Play again? (y/n): ")
        #             if choice.lower() == 'y':
        #                 self.restart_game()
        #             else: break
        #         turn = (turn + 1) % 2
        #     else:
        #         print("Invalid move. Try again.")

    # def restart_game(self):
    #     self._board.create_board()
    #     self._logger = GameLogger()

if __name__ == "__main__":
    g = LocalGame('gomoku')
    g.play()

