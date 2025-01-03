import tkinter as tk
from ..events import Events

class Keybinds:
    def __init__(self, app: tk.Tk):
        self.app_root = app
        self.bind_keys()

    def bind_keys(self):
        # File operations
        self.app_root.bind("<Control-o>", lambda _: Events.trigger("OpenFile"))
        self.app_root.bind("<Control-s>", lambda _: Events.trigger("SaveFile"))
        self.app_root.bind("<Control-Shift-S>", lambda _: Events.trigger("SaveFileAs"))
        
        # Tab management
        self.app_root.bind("<Control-n>", lambda _: Events.trigger("CreateTab"))
        self.app_root.bind("<Control-w>", lambda _: Events.trigger("DestroyTab"))
        
