from utils.event_scope import gui_dispatcher
from utils.events import MovePlacedEvent, GameWonEvent, GameDrawEvent
from gui.events import events

@gui_dispatcher.register(MovePlacedEvent)
def gui_move(event):
    print(f"GUI MOVE: {event.player.name} placed at ({event.x}, {event.y})")
    events.emit("piece_placed", event.x, event.y, event.player.symbol)


@gui_dispatcher.register(GameWonEvent)
def gui_win(event):
    events.emit("game_over", f"{event.winner.name} wins!")

@gui_dispatcher.register(GameDrawEvent)
def gui_draw(event):
    events.emit("game_over", "It's a draw!")

