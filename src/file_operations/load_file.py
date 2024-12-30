from tkinter import messagebox
from os import path
from ..events import Events

class LoadFile:
    @staticmethod
    def load(file_path: str | None = None) -> None:
        """Tries to load the file in path on the text editor"""
        if file_path and path.exists(file_path):
            with open(file_path, "r") as file:
                if file.readable():
                    content: str = file.read()
                    Events.trigger("WriteInEditor", file_path, content, True)
                    Events.trigger("TabSwitch", file_path)
        elif not path.exists(file_path):
            messagebox.showerror("File error", "File does not exist or has been moved.")
