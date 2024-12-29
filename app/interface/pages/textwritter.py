import tkinter as tk
from tkinter.font import Font  
from src.events import Events
from src.file_operations import FileOpenDialog, LoadFile

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
        self.current_file = None

        # Interactive menu
        self.actions_menu = tk.Menu(master.menu, tearoff=0, bg="#21252b", 
                                    fg="#abb2bf", activebackground="#3e4451",
                                    activeforeground="#abb2bf", font=segoe_ui)
        master.menu.configure(bg=self.cget("bg"))
        master.menu.add_cascade(label="File", menu=self.actions_menu)

        # Menu options
        self.actions_menu.add_command(label="Open File", command=self.user_file_path)
        
        # Text Entry
        self.entry = tk.Text(self, bg="#21252b", fg="#abb2bf", font=consolas,
                             insertbackground="#abb2bf", bd=0, highlightthickness=0,
                             selectbackground="#3e4451", selectforeground="#abb2bf")
        self.entry.pack(fill="both", side="left", expand=True)
        
        # Event func
        def switch_file(new_file: str): # Update the current file user is editing
            self.current_file = new_file
            
        
        # Bind events
        Events.bind("WriteInEditor", self.write) # Bind write event to write function
        Events.bind("TabSwitch", switch_file)
        
        # If no file is open, ask for a file. If no file is selected, create a blank tab.
        if len(self.tab_list) == 0:
            self.user_file_path()
      
    def create_tab(self, path: str) -> None:
        """Create a tab for the file.
        Parameters:
        - name: str: Name of the file to be displayed in tab."""
        # Font to be used in tab
        consolas: Font = Font(family="Consolas", size=12, weight="normal")
        
        # Collecting file name from path
        name: str = path.split("/")[-1]
        
        # Creating tab
        self.tab_list[path] = self.tab_list.get(path) or {}
        self.tab_list[path]["Frame"] = tk.Frame(
            master=self.tab_file, bg="#21252b", width=13,
        )
        
        self.tab_list[path]["Button"] = tk.Button(
            master=self.tab_list[path]["Frame"], text=name, font=consolas,
            bg="#21252b", fg="#E1E1E1", bd=0, highlightthickness=0, width=13,
            activebackground="#3e4451", activeforeground="#E1E1E1",
            command=lambda: LoadFile.load(path)
        )
        
        self.tab_list[path]["Close"] = tk.Button(
            master=self.tab_list[path]["Frame"], text="x", font=consolas,
            bg="#21252b", fg="#E1E1E1", bd=0, highlightthickness=0, width=1,
            activebackground="#21252b", activeforeground="#E1E1E1",
            command=lambda: self.destroy_tab(path)
        )
        
        # Updating current file
        self.current_file = path
        
        # Packing tab
        close_bttn: tk.Button = self.tab_list[path]["Close"]
        interact_bttn: tk.Button = self.tab_list[path]["Button"]
        frame: tk.Frame = self.tab_list[path]["Frame"]
        
        close_bttn.pack(side="right")
        interact_bttn.pack(side="right")
        frame.pack(fill="both", side="left")
      
    def destroy_tab(self, path: str, ignore_blank: bool=False) -> None:
        """Destroy a tab on text editor.
        Parameters:
        path: str: Path of the file to be destroyed."""
        if self.tab_list.get(path):
            # Destroying tab & buttons
            self.tab_list[path]["Button"].destroy()
            self.tab_list[path]["Close"].destroy()
            self.tab_list[path]["Frame"].destroy()
            del self.tab_list[path]
            
            # If the file is the current file, load the last file in the tab list
            if path == self.current_file:
                if len(self.tab_list) > 0: # If there are tabs left
                    # Get the last path in tab list
                    last_file_path: str = ""
                    
                    for file in self.tab_list.keys():
                        last_file_path = file
                    
                    # Load the last file in the tab list
                    self.current_file = last_file_path
                    LoadFile.load(self.current_file)
                else:  # If there are no tabs left
                    if not ignore_blank:
                        self.current_file = None
                        self.user_file_path()

    def user_file_path(self) -> None:
        """Ask the user for a file path. If no file is provided, create a blank tab.
        This method also loads the file into the text editor and creates a tab for it."""
        self.update_idletasks()
        file: str | None = FileOpenDialog.ask_open_file()
        
        if file:
            # Destroy untitled tab if it exists
            self.destroy_tab("Untitled", True)
            
            # Load the file and create a tab for it
            LoadFile.load(file)
            self.create_tab(file)
        else:
            if len(self.tab_list) == 0:
                self.create_tab("Untitled")
                self.write(
                    text="NOTE: This file was created automatically and is not saved in any directory. "
                         "If you open a new file or close the program, everything here will be lost unless you save it.", 
                    clear_text=True)

    def write(self, text: str="", clear_text: bool = False) -> None:
        """Overwrite or add text in the entry. Note that this method isn't used by the user.
        It's used only by program to write text in the entry.
        Parameters:
        - text: str: Text to be added to the entry.
        - clear_text: bool: Clear the entry before adding the text."""
        if clear_text:
            self.entry.delete("1.0", tk.END)
        
        self.entry.insert(tk.END, text)
