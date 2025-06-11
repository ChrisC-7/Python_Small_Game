# utils/dispatcher.py

class EventDispatcher:
    def __init__(self, name = None):
        self._handlers = {}
        self.name = name

    def register(self, event_type, func = None):
        if func is None:
            # decorator version
            def wrapper(f):
                self._handlers.setdefault(event_type, []).append(f)
                return f
            return wrapper
        else:
            # direct version
            self._handlers.setdefault(event_type, []).append(func)
    
    def handle(self, event):
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(event)