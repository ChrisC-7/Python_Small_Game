from abc import ABC, abstractmethod
import gameLogic.board as board
import gameLogic.player as player

class IRule(ABC):

    @abstractmethod
    def is_win(self, player: player.Human_Player, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def is_draw(self) -> bool:
        pass


class TicTacToeRule(IRule):

    def __init__(self, board: board.Board, win_condition: int):
        self._board = board
        self._win_condition = win_condition


    def is_win(self, player: player.Human_Player, x: int, y: int) -> bool:
        x_in, y_in = x-1, y-1
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        for dx, dy in directions:
            if self._win_condition <= self._board.check_line(player.symbol, x_in, y_in, dx, dy):
                return True
        return False

    def is_draw(self) -> bool:
        return self._board.check_full()