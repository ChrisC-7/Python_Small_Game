# gui/events.py

class EventBus:
    def __init__(self):
        self.listeners = {}

    ## add all the callback function into our listeners
    def on(self, event_name : str, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit(self, event_name, *args, **kwargs):
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(*args, **kwargs)

events = EventBus()