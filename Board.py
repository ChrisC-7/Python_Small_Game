import Player
from typing import Tuple
from copy import deepcopy

class Board:
    _board = []

    def __init__(self, size = 3):
        """Initialize a object board

        Args:
            size (int, optional): The size of the board 
        """
        self._size = size
        self.create_board()
    
    def create_board(self):
        """Initialize the board list
        """
        self._board =  [[' ' for _ in range(self._size)] for _ in range(self._size)]

    def get_state(self):
        return deepcopy(self._board)
    
    def print_board(self):
        """Print the board  
        """
        for row in range(self._size):
            print(' | '.join(self._board[row]))
            if row != self._size - 1:
                print('-' * (self._size * 4 - 3))
    

    def check_available(self, x: int, y: int) -> bool:
        """ Checks whether the given coordinates are within board boundaries
            and if the cell is unoccupied.
        Args:
            x (int): the row index 
            y (int): the col index

        Returns:
            bool: True if the indexs is in the board and the position is empty
        """
        return self.check_in_board(x,y) and (self._board[x][y] == ' ')
    
    def check_in_board(self, x: int, y: int) -> bool:
        """ Checks whether the given coordinates are within board boundaries 
            and if the cell is unoccupied.
        Args:
            x (int): the row index 
            y (int): the col index

        Returns:
            bool: True if the indexs is in the board
        """
        return 0 <= x < self._size and 0 <= y < self._size
    


    def set_piece(self, x: int, y: int, symbol: str):
        """ Change the position in the board to symbol

        Args:
            x (int): the row index 
            y (int): the col index
            symbol (str): The symbol need to be set
        """
        self._board[x][y] = symbol

    def get_cell(self, x: int, y: int) -> str:
        """get the symbol at board index x, y
        Assumes the given coordinates are within valid board range
    
        Args:
            x (int): the row index
            y (int): the col index

        Returns:
            str: the symbol at the position
        """
        assert self.check_in_board(x, y)
        return self._board[x][y]


     # get how many symbol we have in a line
    def check_line(self, x: int, y: int, dx: int, dy: int) -> int:
        """Counts the number of consecutive identical symbols in a line 
            passing through the given position.

        Args:
            x (int): the row index
            y (int): the col index
            dx (int): how we increment the row
            dy (int): hoe we increase the col

        Returns:
            int: the amount of pieces in one line
        """
        count = 0
        symbol = self.get_cell(x, y) 
        x_in_Board, y_in_Board = x, y  
        while(self.check_in_board(x_in_Board, y_in_Board) and self.get_cell(x_in_Board, y_in_Board) == symbol ):
            count += 1
            x_in_Board += dx
            y_in_Board += dy

        x_in_Board, y_in_Board = x - dx, y - dy
        while(self.check_in_board(x_in_Board, y_in_Board) and self.get_cell(x_in_Board, y_in_Board) == symbol ):
            count += 1
            x_in_Board -= dx
            y_in_Board -= dy
        return count

    def check_full(self) -> bool:
        """Check if the board is full

        Returns:
            bool: true if the board if full
        """  
        return all(cell != ' ' for row in self._board for cell in row)

    def place_piece(self, x: int, y: int, symbol: str) -> bool:
        """Places the symbol into the board

        Args:
            symbol (str): The symbol need to be place
            x (int): row index
            y (int): col index

        Returns:
            bool: True if place successfully
        """
        if(self.check_available(x, y)): 
            self.set_piece(x, y, symbol)
            return True
        return False

    def __str__(self):
            result = "    " + "   ".join(str(i) for i in range(self._size)) + "\n"
            for i, row in enumerate(self._board):
                row_str = " | ".join(_ for _ in row)
                result += f"{i} | {row_str} |\n"
                if i < self._size - 1:  
                    result += " " + "-----" * self._size + "\n"
            
            return result


