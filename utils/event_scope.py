# utils/event_scope.py

from utils.dispatcher import EventDispatcher

cli_dispatcher = EventDispatcher("CLI")
gui_dispatcher = EventDispatcher("GUI")
