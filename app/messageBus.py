class MessageBus(object):
    def __init__(self):
        self.handlers = {}

    def register_handler(self, event, handler):
        if event in self.handlers:
            self.handlers[event].append(handler)
        else:
            self.handlers[event] = [handler]

    def fire_event(self, event, **params):
        if event not in self.handlers:
            return

        for handler in self.handlers[event]:
            result = handler(**params)
            if result:
                return result