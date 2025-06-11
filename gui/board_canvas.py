# gui/board_canvas.py

import tkinter as tk
from gui.events import events


class BoardCanvas(tk.Canvas):
    def __init__(self, master, size = 15, cell_size = 40, padding = 20):
        super().__init__(master, bg = 'burlywood', 
                       width = size * cell_size + padding * 2,
                       height = size * cell_size + padding * 2)
        self.size = size
        self.cell_size = cell_size
        self.padding = padding
        self.bind("<Button-1>", self._on_click)

    def draw_board(self):
        self.delete("all")

        for i in range(self.size):
            start = self.padding
            end = self.padding + (self.size - 1) *self.cell_size
            offset = self.padding + i * self.cell_size
            self.create_line(start, offset, end, offset)
            self.create_line(offset, start, offset, end)

    def draw_piece(self, row, col, symbol):
        col = col - 1 
        row = row - 1
        x = self.padding + col * self.cell_size
        y = self.padding + row * self.cell_size
        r = self.cell_size // 2 - 2
        color = "black" if symbol == "X" or symbol == "x" else "white"
        self.create_oval(x - r, y - r, x + r, y + r, fill = color, outline="black")
    
    def _on_click(self,event):
        row = (event.y - self.padding + self.cell_size // 2) // self.cell_size
        col = (event.x - self.padding + self.cell_size // 2) // self.cell_size
        print(f"Click at: ({row}, {col})")
        events.emit("board_click", row+1, col+1)
        # x = event.x - self.padding
        # y = event.y - self.padding

        # if x < 0 or y < 0:
        #     return  # 忽略点击在 padding 区域的情况

        # row = y // self.cell_size
        # col = x // self.cell_size

        # # 再次确认不越界
        # if 0 <= row < self.size and 0 <= col < self.size:
        #     events.emit("board_click", row+1, col+1)