from tkinter import messagebox
from os import path
from . import FileSaveDialog
from ..events import Events
from tempfile import gettempdir
from os import remove
from os.path import dirname, exists

class SaveFile:
    @staticmethod
    def save(content: str, file_path: str | None=None, can_create: bool=False):
        """Save the file with provided content. If file_path is nil
        So function will ask the user to 'Save as'
        
        Parameters:
        - content: The content (text) to override the file content
        - file_path: The path where file to be overrided is located
        - can_create: If true, it will create the file if the file doesn't exists
        - cancel_event: If true, it will not fire TabSwitch event"""
        
        if file_path: # Check if file exists
            # Asks to save as new if file doesn't exists and function aren't able to create
            if (not can_create and not path.exists(file_path)
                    or dirname(file_path) == gettempdir()):
                Events.trigger("DestroyTab", file_path, True)
                SaveFile.save_as(content, file_path)
                return
            
            # Save file
            with open(file_path, "w") as file:
                if file.writable():
                    file.truncate(0)
                    file.write(content[:-1:])
                    
                    Events.trigger("FileSaved", file_path)
                    Events.trigger("TabSwitch", file_path)
                else: # File can't be writted
                    messagebox.showwarning("File can't be writed",
                                           "The current file can't be written."
                                           "The save hasn't been done.")
        else:
            SaveFile.save_as(content)
    
    @staticmethod
    def save_as(content: str, file_path: str | None = None):
        """Create a file with the provided name.
        
        Parameters:
        - content: The content (text) to create the file with
        - file_path: Optional. Path to a blank file"""
        new_file_path: str | None = FileSaveDialog.ask_save_as()
                
        if new_file_path: # If user created a file
            Events.trigger("DestroyTab", file_path or "blank", True)
            SaveFile.save(content, new_file_path, True) # Implements a recursion to save
            Events.trigger("TabSwitch", new_file_path)
            
            if (file_path and dirname(file_path) == gettempdir()
                    and exists(file_path)):
                remove(file_path)
