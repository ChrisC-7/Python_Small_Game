# gui/components.py 

from tkinter import ttk
from gui.events import events

class ControlPanel(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack(pady = 5)
        self.restart_btn = ttk.Button(self, text="Restart", command=self.restart_game)
        self.restart_btn.pack()
    
    def restart_game(self):
        events.emit("restart")