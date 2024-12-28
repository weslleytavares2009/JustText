import tkinter as tk
from tkinter.font import Font  
from src.events import Events
from src.file_operations import FileOpenDialog, LoadFile

# TODO: Must implement the tab creation when a file is opened 
# with the action "Open File" in the menu.

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
        self.tab_list = {}

        # Interactive menu
        self.actions_menu = tk.Menu(master.menu, tearoff=0, bg="#21252b", 
                                    fg="#abb2bf", activebackground="#3e4451",
                                    activeforeground="#abb2bf", font=segoe_ui)
        master.menu.configure(bg=self.cget("bg"))
        master.menu.add_cascade(label="File", menu=self.actions_menu)

        self.actions_menu.add_command(label="Open File",
                                      command=lambda: LoadFile.load(
                                          FileOpenDialog.ask_open_file()))
        
        # Text Entry
        self.entry = tk.Text(self, bg="#21252b", fg="#abb2bf", font=consolas,
                             insertbackground="#abb2bf", bd=0, highlightthickness=0,
                             selectbackground="#3e4451", selectforeground="#abb2bf")
        self.entry.pack(fill="both", side="left", expand=True)
        
        # Bind events
        Events.bind("WriteInEditor", self.write) # Bind write event to write function
        
        # If no file is open, ask for a file. If no file is selected, create a blank tab.
        if len(self.tab_list) == 0:
            self.update_idletasks()
            file: str | None = FileOpenDialog.ask_open_file()
            
            if file:
                LoadFile.load(file)
                self.create_tab(file.split("/")[-1])
        self.update_idletasks()
      
    def create_tab(self, name: str):
        """Create a tab for the file.
        Parameters:
        - name: str: Name of the file to be displayed in tab."""
        # Font to be used in tab
        # segoe_ui: Font = Font(family="Segoe UI", size=10, weight="normal")
        consolas: Font = Font(family="Consolas", size=12, weight="normal")
        
        # Creating tab
        self.tab_list[name] = tk.Button(self.tab_file, text=name, font=consolas,
                        bg="#21252b", fg="#E1E1E1", bd=0, highlightthickness=0, width=15,
                        activebackground="#3e4451", activeforeground="#E1E1E1")
        self.tab_list[name].pack(fill="both", side="left")
      
    def write(self, text: str="", clear_text: bool = False):
        """Overwrite or add text in the entry.
        Parameters:
        - text: str: Text to be added to the entry.
        - clear_text: bool: Clear the entry before adding the text."""
        if clear_text:
            self.entry.delete("1.0", tk.END)
        
        self.entry.insert(tk.END, text)
