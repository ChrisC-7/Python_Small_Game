import Player
class Board:
    _size = 0
    _board = []
    def __init__(self, size = 3):
        self._size = size
        self.creatBoard(size)
    
    def creatBoard(self, size = 3):
        self._board =  [[' ' for _ in range(size)] for _ in range(size)]

    def print_board(self):
        for row in range(self._size):
            print(' | '.join(self._board[row]))
            if row != self._size - 1:
                print('-' * (self._size * 4 - 3))

    
    def check_available(self, x, y):
        x_in, y_in = self.convert_to_board_index(x, y)
        return self.check_in_board(x_in,y_in) and (self._board[x_in][y_in] == ' ')
    
    def check_in_board(self, x, y):
        if(x >= self._size or y >= self._size or x < 0 or y < 0 ):
            return False
        return True
    
    def set_piece(self, x, y, player:Player.Player):
        self._board[x][y] = player._symbol



    def get_cell(self, x, y):
        """ get the symbol at board index x, y
        """
        return self._board[x][y]


     # get how many symbol we have in a line
    def check_line(self, x, y, dx, dy):

        x_in_Board, y_in_Board = self.convert_to_board_index(x, y)
        count = 0
        symbol = self.get_cell(x_in_Board, y_in_Board)        
        while(self.get_cell(x_in_Board, y_in_Board) == symbol and self.check_in_board(x_in_Board, y_in_Board)):
            count += 1
            x_in_Board += dx
            y_in_Board += dy

        x_in_Board, y_in_Board = self.convert_to_board_index(x, y)
        x_in_Board -= dx
        y_in_Board -= dy
        while(self.get_cell(x_in_Board, y_in_Board) == symbol and self.check_in_board(x_in_Board, y_in_Board)):
            count += 1
            x_in_Board -= dx
            y_in_Board -= dy
        
        return count





