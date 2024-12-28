import tkinter as tk
from .interface.pages.textwritter import TextWritter

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
        
        # Init
        self.switch_frame(self.pages[0])

    def switch_frame(self, frame: tk.Frame):
        """Switch the current window (frame) to the given frame"""
        for other_frame in self.pages:
            other_frame.pack_forget()
        
        frame.pack(fill="both", expand=True)
        frame.update()
