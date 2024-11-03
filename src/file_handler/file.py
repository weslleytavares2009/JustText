from tkinter import Event, messagebox, filedialog, END
from src.file_handler.changes_save import SaveChanges
from json import load
from io import TextIOWrapper
import os

class LoadFromFile:
    """Tries to load a file source into code editor."""

    @staticmethod
    def load(tkEvent: Event = None, file_path: str = None):
        """Loads a file. If a path file isn't defined, asks to create a new file

        @param tkEvent: Auto-Assignable for tkinter bindable functions
        @param file_path: A path to file (Optional)"""
        from src.editor_style.editor import Editor

        if file_path and not os.path.exists(file_path):
            messagebox.showwarning(file_path, "Failed to load file. File doesn't exists.")
            return

        file: TextIOWrapper | None = (file_path and open(file_path, "r")
                                      or AskForFile.askforfile(throw_error=True))
        if file:
            # Tries to add file to editing list
            if not SaveChanges.search(file.name):
                SaveChanges.push(file_path=file.name)

            # Proceed to load file
            if file.readable():
                Editor.text_writer.delete("1.0", END)

                for lineText in file.readlines():
                    Editor.text_writer.insert(END, lineText)

            file.close()

class LoadFromSave:
    "Loads the entire save from user"
    @staticmethod
    def load():
        with open(SaveChanges.data_path, "r") as data:
            data = load(data)
            for file_info in data["opened_files"]:
                LoadFromFile.load(file_path = file_info[0])

class SaveCurrentFile:
    """Save the current editing file"""
    def save(event: Event = None, close_on_save: bool = False):
        """Save the current opened file.
        @param event: Tkinter event (auto-assignable)
        @param close_on_save: If should close the file on editor after save"""
        
        from src.editor_style.editor import Editor
        current_file: tuple[str, int] | None = SaveChanges.peek()
        if current_file and os.path.exists(current_file[0]):
            file: TextIOWrapper | None = open(current_file[0], "w")

            if file:
                file.truncate(0)
                file.write(Editor.text_writer.get('1.0', END)) 
                
                print(Editor.modified_files)
                if file.name in Editor.modified_files:
                    Editor.modified_files.remove(file.name)
                    print(Editor.modified_files)
                    
                file.close()
                
                #* Not implemented yet.
                
                # if close_on_save:
                #     with open(SaveChanges.data_path) as data:
                #         opened_files: list[list[str, int]] = data["opened_files"]
                #         opened_files.pop(0)
            
class SaveFileAs:
    """Save a file as a specified name & type"""
    def save(event: Event):
        """Save a file as a specified name & type"""
        file: TextIOWrapper | None = AskForFile.askforfile(2, "w", True, True)

        if file:
            LoadFromFile.load(file_path = file.name)

class AskForFile:
    """Handles user interations (I/O) to open/save a file"""

    @staticmethod
    def askforfile(
        state: int = 1, mode: str = "r",
        throw_error: bool = False, add_to_list: bool = False) -> TextIOWrapper | None:
        """Handles user interations to open/save a file.

        @param state: State defines which type of gui should appear.
        Use 1 for Open file and 2 to Save file.

        @param mode: How file should be opened if sucessful. Similar to open() method.

        @param add_to_list: Should the file automatically be added to editing files list?

        @param throw_error: If program should throw an error window if something failed.
        It doesn't stop application from running. Return None instead."""

        user_input: TextIOWrapper | None

        # Switch case implementation to alternate between "ask" properties
        match state:
            case 1:
                user_input = filedialog.askopenfile(mode)
            case 2:
                user_input = filedialog.asksaveasfile(mode)

        # Show error if file isn't valid and throw error are enabled.
        if type(user_input) != TextIOWrapper and throw_error:
            messagebox.showwarning("Operation Failed", "Failed to open/save that file.")
            return None

        # Tries to insert file into PriorityQueue
        if add_to_list:
            if not SaveChanges.search(user_input.name):
                SaveChanges.push(user_input.name)

        return user_input
