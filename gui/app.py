# gui/app.py

import tkinter as tk
from tkinter import ttk
from gui.board_canvas import BoardCanvas
from gui.controller import GameController
from gui.components import ControlPanel
from gui.events import events
import utils.gui_dispatcher_using  # 👈 这是激活 handler 注册的关键



class GomokuApp(tk.Tk):
    def __init__(self):
        # import pdb; pdb.set_trace()
        super().__init__()
        self.title("Modular Gomoku Game")
        
        self.controller = GameController()
        
        self.canvas = BoardCanvas(self)
        self.canvas.pack()
        self.canvas.draw_board()

        self.control_panel = ControlPanel(self)
        
        self.status_label = ttk.Label(self, text="Welcome!")
        self.status_label.pack(pady=5)

        events.on("piece_placed", self.canvas.draw_piece)
        events.on("game_over", self.show_game_result)
        events.on("ai_turn", lambda _: self.after(500, self.controller.ai_move))
        events.on("restart", self.reset_board)

    def show_game_result(self, message):
        self.status_label.config(text=message)

    def reset_board(self):
        self.canvas.draw_board()
        self.status_label.config(text="New Game Started!")

if __name__ == "__main__":
    app = GomokuApp()
    app.mainloop()
