class Events:
    binds: dict[str: list[callable]] = {}
    
    @staticmethod
    def bind(event_name: str, func: callable) -> None:
        """Bind a function to an event"""
        # Creating event if event does not exist
        if not event_name in Events.binds:
            Events.binds[event_name] = []
        
        # Adding function to event if function is not already in event
        if not func in Events.binds[event_name]:
            Events.binds[event_name].append(func)
    
    @staticmethod
    def unbind(event_name: str, func: callable):
        """Unbind a function from an event"""
        try:
            Events.binds[event_name].remove(func)
        except ValueError:
            pass # Ignore if function is not in event. No need to raise an error.
    
    @staticmethod
    def trigger(event_name: str, *args, **kwargs):
        """Trigger an event"""
        if event_name in Events.binds:
            for callback in Events.binds[event_name]:
                callback(*args, **kwargs)
