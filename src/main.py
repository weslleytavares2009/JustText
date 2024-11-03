from src.editor_style.editor import Editor
from src.functions import Loader
from src.file_handler.changes_save import SaveChanges
from src.file_handler.file import SaveCurrentFile
from json import load
from tkinter import Event, messagebox, END

class App():
    def __init__(self):
        #* Initializing editor appearence
        Editor.create_body()
        
        #* Loading editor extra functionalities
        #? Undo-Redo, Auto-Save & etc...
        Loader.initialize()
        
        Editor.load_keybinds()

    @staticmethod
    def run():
        Editor.run_program()

    @staticmethod
    def shutdown():
        if not Editor.closing:
            Editor.closing = True

            # Save unsaved changes
            #! WARNING: May be slow with multiple large sized files
            
            if len(Editor.modified_files) > 0:
                user_choice: bool = messagebox.askyesno(
                    "Save unsaved changes",
                    "You have unsaved changes. Do you want to save it before exit?"
                )
                
                if user_choice == True:
                    SaveCurrentFile.save()
                
            Editor.program.quit()

if __name__ == "__main__":
    App()
