import tkinter as tk
from tempfile import TemporaryFile, gettempdir
from tkinter.font import Font  
from src.events import Events
from src.file_operations import FileOpenDialog, LoadFile, SaveFile
from os.path import dirname, exists
from os import remove

class TextWritter(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        master: tk.Tk = args[0]

        # Style
        self.configure(bg="#282c34")

        # Fonts
        segoe_ui: Font = Font(family="Segoe UI", size=10, weight="normal")

        # Files tab
        self.tab_file = tk.Canvas(self, bg=self.cget("bg"), height=0, bd=0, highlightthickness=0)
        self.tab_file.pack(fill="x", side="top")
        
        self.tab_list = {}
        self.editing_list = []
        self.current_file = None

        # Interactive menu
        self.actions_menu = tk.Menu(master.menu, tearoff=0, bg="#21252b", 
                                    fg="#abb2bf", activebackground="#3e4451",
                                    activeforeground="#abb2bf", font=segoe_ui)
        master.menu.configure(bg=self.cget("bg"))
        master.menu.add_cascade(label="File", menu=self.actions_menu)

        # Lambdas
        get_text = lambda: self.tab_list[self.current_file]["Entry"].get("1.0", tk.END)

        # Menu options
        self.actions_menu.add_command(label="Open File", command=self.user_file_path)
        self.actions_menu.add_command(label="Save File", 
                                      command=lambda: SaveFile.save(
                                          get_text(),
                                          self.current_file
                                        ))
        self.actions_menu.add_command(label="Save as File",
                                      command=lambda: SaveFile.save_as(
                                          get_text()
                                      ))

        # Event func
        def switch_file(new_file: str):
            """Switch opened file"""
            # Create a new tab for the file (if there's none)
            if not self.tab_list.get(new_file):
                self.create_tab(new_file)
            
            # Hide files
            self.hide_texts(new_file)
            self.current_file = new_file
            
        def on_file_saved(file_path: str):
            """Called when a file is sucessfully saved. It removes the file from editing list."""
            if file_path in self.editing_list:
                self.editing_list.remove(file_path)
        
        # Bind events
        Events.bind("WriteInEditor", self.write)
        Events.bind("TabSwitch", switch_file)
        Events.bind("FileSaved", on_file_saved)
        
        # Keybinds (Still events)
        Events.bind("OpenFile", self.user_file_path)
        Events.bind("SaveFile", lambda: SaveFile.save(get_text(), self.current_file))
        Events.bind("SaveFileAs", lambda: SaveFile.save_as(get_text()))
        Events.bind("CreateTab", self.create_temp_file)
        Events.bind("DestroyTab", lambda: self.destroy_tab(self.current_file))
        
        # Create a blank tab.
        self.create_temp_file()
      
    def create_tab(self, path: str) -> None:
        """Create a tab for the file.
        
        Parameters:
        - name: str: Name of the file to be displayed in tab."""
        # Return if tab already exists
        if self.tab_list.get(path):
            return
        
        # Font to be used in tab
        consolas: Font = Font(family="Consolas", size=12, weight="normal")
        
        # Returns an unique name for temp files
        def best_temp_name() -> str:
            """Gets the best unique name for temporary/unsaved files."""
            highest_blank: int = 0
            
            for tab_path in self.tab_list.values():
                # Button label
                file_label: str = tab_path["Button"].cget("text")
                
                if file_label == "Untitled":
                    highest_blank = 1
                    continue
                    
                split_tab: list[str] = file_label.split("Untitled")
                if len(split_tab) > 0:
                    try:
                        highest_blank = int(split_tab[-1]) + 1
                    except ValueError:
                        pass # No needs to threat the error
                    
            return highest_blank > 0 and f"Untitled {highest_blank}" or "Untitled"
        
        # Collecting file name. Name it's visual only
        is_temp_file: bool = gettempdir() == dirname(path) # check if file is temporary
        name: str = is_temp_file and best_temp_name() or path.split("/")[-1]
        
        # Function to be called whwen the tab button be clicked
        def interact_tab() -> None:
            self.hide_texts(path)
            
            if self.tab_list.get(path):
                self.current_file = path
        
        # Creating tab
        self.tab_list[path] = {}
        self.tab_list[path]["Frame"] = tk.Frame(
            master=self.tab_file, bg="#21252b", width=13,
        )
        
        self.tab_list[path]["Button"] = tk.Button(
            master=self.tab_list[path]["Frame"], text=name, font=consolas,
            bg="#21252b", fg="#E1E1E1", bd=0, highlightthickness=0, width=13,
            activebackground="#3e4451", activeforeground="#E1E1E1",
            command=interact_tab
        )
        
        self.tab_list[path]["Close"] = tk.Button(
            master=self.tab_list[path]["Frame"], text="x", font=consolas,
            bg="#21252b", fg="#E1E1E1", bd=0, highlightthickness=0, width=1,
            activebackground="#21252b", activeforeground="#E1E1E1",
            command=lambda: self.destroy_tab(path)
        )
        
        self.tab_list[path]["Entry"] = tk.Text(self, bg="#21252b", fg="#abb2bf", font=consolas,
                             insertbackground="#abb2bf", bd=0, highlightthickness=0,
                             selectbackground="#3e4451", selectforeground="#abb2bf")
        
        # Updating current file
        self.current_file = path
        
        # Setting default text content (if it's a temp file)
        if is_temp_file:
            self.write(
                        filepath=self.tab_list[path]["Entry"],
                        text="NOTE: This file was created automatically and is not saved in any directory. "
                            "If you open a new file or close the program, everything here will be lost unless you save it.", 
                        clear_text=True)
        
        # Packing tab
        close_bttn: tk.Button = self.tab_list[path]["Close"]
        interact_bttn: tk.Button = self.tab_list[path]["Button"]
        frame: tk.Frame = self.tab_list[path]["Frame"]
        entry: tk.Text = self.tab_list[path]["Entry"]
        
        entry.pack(fill="both", side="left", expand=True)
        close_bttn.pack(side="right")
        interact_bttn.pack(side="right")
        frame.pack(fill="both", side="left")
        
        # Binding events
        def on_typing(event: tk.Event):
            """Called when user types anything in file."""
            if not path in self.editing_list:
                self.editing_list.append(path)
        
        entry.bind("<KeyPress>", on_typing)
    
    def destroy_tab(self, path: str, ignore_blank: bool=False) -> None:
        """Destroy a tab on text editor.
        
        Parameters:
        path: Path of the file to be destroyed.
        ignore_blank: If there's no tab open, don't ask user to open a file"""
        if self.tab_list.get(path):
            # Destroying tab & buttons
            self.tab_list[path]["Button"].destroy()
            self.tab_list[path]["Close"].destroy()
            self.tab_list[path]["Frame"].destroy()
            self.tab_list[path]["Entry"].destroy()
            del self.tab_list[path]
            
            # If the file is a blank file, destroy the temp file
            # TODO: Later, I will to add a feature to ask if user wants to save changes
            if gettempdir() == dirname(path) and exists(path):
                remove(path)
                
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

    def hide_texts(self, exception: str | None = None):
        """Hide every text input (entry)
        
        Parameters:
        - exception: Hide all entries EXCEPT entry for this path"""
        # Updating entry visibility
        for filename, value in self.tab_list.items():
            entry: tk.Text = value["Entry"]
            entry.pack_forget()
                    
            if exception and filename == exception:
                entry.pack(fill="both", side="left", expand=True)

    def create_temp_file(self) -> None:
        """Creates a temporary file. AKA Blank, Empty or Untitled file.
        Also create a new tab for it.
        
        Parameters:
        - cancel_tab_switch: If true, it will not fire TabSwitch"""
        pathname: str = ""

        with TemporaryFile(mode="w", delete=False, delete_on_close=False) as f:
            pathname = f.name
            f.close()
            
        LoadFile.load(pathname)
        self.create_tab(pathname)
        
        # entry: tk.Text = self.tab_list[pathname]["Entry"]
        # SaveFile.save(entry.get("1.0", tk.END), pathname)

    def user_file_path(self) -> None:
        """Ask the user for a file path. If no file is provided, create a blank tab.
        This method also loads the file into the text editor and creates a tab for it."""
        self.update_idletasks()
        file: str | None = FileOpenDialog.ask_open_file()
        
        if file:
            # Load the file and create a tab for it
            self.create_tab(file)
            self.hide_texts(exception=file)
            LoadFile.load(file)
        else:
            if len(self.tab_list) == 0:
                self.create_temp_file()

    def write(self, filepath: str, text: str="", 
              clear_text: bool = False) -> None:
        """Overwrite or add text in the entry. Note that this method isn't used by the user.
        It's used only by program to write text in the entry.
        
        Parameters:
        - text: str: Text to be added to the entry.
        - clear_text: bool: Clear the entry before adding the text."""
        if self.tab_list.get(filepath):
            entry: tk.Text = self.tab_list[filepath]["Entry"]
            
            if clear_text:
                entry.delete("1.0", tk.END)
            
            entry.insert(tk.END, text)
