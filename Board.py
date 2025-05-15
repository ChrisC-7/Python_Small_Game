class Board:
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
