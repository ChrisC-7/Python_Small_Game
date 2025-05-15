import Board 
import Player
from typing import Tuple
from Rule import TicTacToeRule

class Game:

    def __init__(self, player_amount = 2, win_condition = 3 ):
        """_summary_

        Args:
            player_amount (int, optional): The player's amount for the game. Defaults to 2.
            win_condition (int, optional): The winning condition for this game. Defaults to 3.
        """

        self._board = Board.Board()
        self._player_amount = player_amount
        self._players = []
        self._win_condition = win_condition
        self._rule = TicTacToeRule(self._board, self._win_condition) 
        self.init_players()
    
    def init_players(self):
        """Initilize the list for the players
        """

        for i in range(self._player_amount):        
            name = input("Please input player's name: ")
            symbol = input("Which symbol does this player want to use: ")
            self._players.append(Player.Player(i, name, symbol))
    
    def convert_to_board_index(self, x: int, y: int) -> Tuple[int, int]:
        """ Converts user's input coordinates to board indexs

        Args:
            x (int): user's inpot row
            y (int): user's input col

        Returns:
            Tuple[int, int]: The index in the board
        """
        return x-1, y-1
    
    def current_player(self, order: int) -> Player.Player:
        """Gets the current player

        Args:
            order (int): the play order

        Returns:
            Player.Player: The current player
        """

        return self._players[order]

    def place_piece(self, symbol: str, x: int, y: int) -> bool:
        """Places the symbol into the board

        Args:
            symbol (str): The symbol need to be place
            x (int): row index
            y (int): col index

        Returns:
            bool: True if place successfully
        """
        x_in, y_in = self.convert_to_board_index(x, y)
        if(self._board.check_available(x_in, y_in)): 
            self._board.set_piece(x_in, y_in, symbol)
            return True
        return False
    
    def make_move(self, player:Player.Player) -> Tuple[int, int]:
        """Player makes move

        Args:
            player (Player.Player): The play who is going make move

        Returns:
            Tuple[int, int]: The row and col
        """

        while True:
            x = int(input("The x place you want to do: "))
            y = int(input("The y place you want to do: "))
            if self.place_piece(player.symbol, x, y):
                return x, y
            print("Please enter valid x, y")


    # def check_win(self, player: Player.Player, x: int, y: int) -> bool:
    #     """Wheather the player wins

    #     Args:
    #         player (Player.Player): play who is checking winning now
    #         x (int): row index
    #         y (int): col index

    #     Returns:
    #         bool: true if the play wins
    #     """
    #     x_in, y_in = self.convert_to_board_index(x, y)
    #     directions = [(1,0), (0,1), (1,1), (1,-1)]
    #     for dx, dy in directions:
    #         if self._win_condition <= self._board.check_line(x_in, y_in, dx, dy):
    #             player.mark_as_winner()
    #             return True
    #     return False

    def check_draw(self) -> bool:
        """Whether the game is a draw

        Returns:
            bool: whether the game is a draw
        """
        return self._board.check_full()
    
    def display_board(self):
        """show the 2D board
        """
        print("\nCurrent board state:")
        self._board.print_board()

    def play(self):
        """The logic of the game 
        """
        a = 0
        while True:
            player = self.current_player(a)
            print(f"Player {player.name} 's turn")
            x, y = self.make_move(player)
            self.display_board()
            if self._rule.is_win(player,x, y):
               player.mark_as_winner
               print(f"Player {player.name} wins!")
               break
            if self._rule.is_draw():
                print("Game is draw")
                break
            a = (a + 1) % self._player_amount

if __name__ == "__main__" :
    g = Game()
    g.play()


        

