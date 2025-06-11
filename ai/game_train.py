import numpy as np

class Game:
    def __init__(self, board_size = 5, win_condirion = 4):
        self.board_size = board_size
        self.win_condition = win_condirion
        self.board = np.zeros(board_size, board_size)
        self.current_player = 1
        self.move = []
