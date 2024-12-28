import tkinter as tk
from ..events import Events

class LoadFile:
    @staticmethod
    def load(file_path: str | None = None) -> None:
        """Tries to load the file in path on the text editor"""
        if file_path:
            with open(file_path, "r") as file:
                if file.readable():
                    text = file.read()
                    Events.trigger("WriteInEditor", text, True)
