import tkinter as tk
from tkinter.font import Font

class TextWritter(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        master: tk.Tk = args[0]

        # Style
        self.configure(bg="#282c34")

        # Fonts
        consolas: Font = Font(family="Consolas", size=12, weight="normal")
        segoe_ui: Font = Font(family="Segoe UI", size=10, weight="normal")

        # Files tab
        self.tab_file = tk.Canvas(self, bg=self.cget("bg"), height=0, bd=0, highlightthickness=0)
        self.tab_file.pack(fill="x", side="top")

        self.tab_file.test2 = tk.Button(self.tab_file, text="main.py", font=segoe_ui,
                                        bg="#21252b", fg="#abb2bf", bd=0, highlightthickness=0, width=15,
                                        activebackground="#3e4451", activeforeground="#abb2bf")
        self.tab_file.test2.pack(fill="both", side="left")

        # Interactive menu
        self.actions_menu = tk.Menu(master.menu, tearoff=0, bg="#21252b", fg="#abb2bf", activebackground="#3e4451", activeforeground="#abb2bf", font=segoe_ui)
        master.menu.add_cascade(label="File", menu=self.actions_menu)

        self.actions_menu.add_command(label="Open File", command=lambda: print("Opening file"))
        
        # Text Entry
        self.entry = tk.Text(self, bg="#21252b", fg="#abb2bf", font=consolas,
                             insertbackground="#abb2bf", bd=0, highlightthickness=0, selectbackground="#3e4451", selectforeground="#abb2bf")
        self.entry.pack(fill="both", side="left", expand=True)
