import tkinter as tk
from .interface.pages.textwritter import TextWritter
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window property
        self.screenWidth: int = self.winfo_screenwidth()
        self.screenHeight: int = self.winfo_screenheight()

        # Setup window
        self.geometry(f"{self.screenWidth // 2}x{self.screenHeight // 2}")
        self.title("JustText")
        self.configure(bg="#282c34")
        self.menu = tk.Menu(self, tearoff=0, bg="#21252b", fg="#abb2bf", activebackground="#3e4451", activeforeground="#abb2bf", font=("Segoe UI", 10))
        self.config(menu=self.menu)

        # App thing
        self.pages: list[tk.Frame] = [TextWritter(self)]
        
        # Bindings
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Init
        self.switch_frame(self.pages[0])

    def on_closing(self):
        """Called when the window is destroyed."""
        # TODO: Ask the user if he wants to save changes
        
        # Get the opened files to destroy tabs & temporary files
        opened_files: dict = self.pages[0].tab_list.copy() # Copy the dict because it will be modified
        
        for file_path in opened_files.keys():
            self.pages[0].destroy_tab(file_path, True)
            
        # Destroying references
        opened_files.clear()
        opened_files = None
        
        self.quit() # This method will destroy the window properly.

    def switch_frame(self, frame: tk.Frame):
        """Switch the current window (frame) to the given frame"""
        for other_frame in self.pages:
            other_frame.pack_forget()
        
        frame.pack(fill="both", expand=True)
        frame.update()
