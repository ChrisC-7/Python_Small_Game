import Board 
import Player

class Game:

    def __init__(self, player_number = 2, win_condition = 3 ):
        self._board = Board.Board()
        self._play_number = player_number
        self._players = []
        self._win_condition = win_condition
        self.init_players()
    
    def init_players(self):
        for i in range(self._play_number):        
            name = input("Please input player's name: ")
            symbol = input("Which symbol does this player want to use: ")
            self._players.append(Player.Player(i, name, symbol))
    
    def convert_to_board_index(self, x, y):
        return x-1, y-1
    
    def place_piece(self, player: Player.Player) -> bool:
        x = int(input("The x place you want to do: "))
        y = int(input("The y place you want to do: "))
        x_in, y_in = self.convert_to_board_index(x, y)
        if(self._board.check_available(x_in, y_in)): 
            self._board.set_piece(x_in, y_in, player)
            return True
        return False

        

