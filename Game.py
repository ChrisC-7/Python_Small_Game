import Board 
import Player

class Game:

    def __init__(self, player_amount = 2, win_condition = 3 ):
        self._board = Board.Board()
        self._player_amount = player_amount
        self._players = []
        self._win_condition = win_condition
        self.init_players()
    
    def init_players(self):
        for i in range(self._player_amount):        
            name = input("Please input player's name: ")
            symbol = input("Which symbol does this player want to use: ")
            self._players.append(Player.Player(i, name, symbol))
    
    def convert_to_board_index(self, x, y):
        return x-1, y-1
    
    def current_player(self, order) -> Player.Player:
        return self._players[order]

    def place_piece(self, symbol: str, x, y) -> bool:
        
        x_in, y_in = self.convert_to_board_index(x, y)
        if(self._board.check_available(x_in, y_in)): 
            self._board.set_piece(x_in, y_in, symbol)
            return True
        return False
    
    def make_move(self, player:Player.Player):
        while True:
            x = int(input("The x place you want to do: "))
            y = int(input("The y place you want to do: "))
            if self.place_piece(player.symbol, x, y):
                return x, y
            print("Please enter valid x, y")


    def check_win(self, player: Player.Player, x, y) -> bool:
        x_in, y_in = self.convert_to_board_index(x, y)
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        for dx, dy in directions:
            if self._win_condition <= self._board.check_line(x_in, y_in, dx, dy):
                player.mark_as_winner()
                return True
        return False

    def check_draw(self):
        return self._board.check_full()
    
    def display_board(self): 
        print("\nCurrent board state:")
        self._board.print_board()

    def play(self):
        a = 0
        while True:
            player = self.current_player(a)
            print(f"Player {player.name} 's turn")
            x, y = self.make_move(player)
            self.display_board()
            if self.check_win(player,x, y):
               print(f"Player {player.name} wins!")
               break
            if self.check_draw():
                print("Game is draw")
                break
            a = (a + 1) % self._player_amount

if __name__ == "__main__" :
    g = Game()
    g.play()


        

