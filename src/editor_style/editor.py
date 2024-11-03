import tkinter as tk
from tkinter.font import Font
import src.file_handler.file as file_util
from src.functions import run_file

class Editor:
    # Static variables for UI Elements
    program: tk.Tk | None = None
    main_frame: tk.Frame | None = None
    text_writer: tk.Text | None = None
    text_scroll: tk.Scrollbar | None = None
    string_var: tk.StringVar | None = None
    closing: bool = False
    
    # Modified files (stores files path)
    modified_files: list[str] = []

    @staticmethod
    def run_program():
        if Editor.program:  # Checks if the window has been created
            Editor.program.mainloop()

    @staticmethod
    def create_body():
        """Design front-end application appearence"""
        Editor.program = tk.Tk()  # Creates the main window
        Editor.program.title("JustText")  # Set the title

        # Creates a frame for better padding and structure
        Editor.frame = tk.Frame(Editor.program, bg='#2E302F')
        Editor.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Where the text will be written
        text_font: Font = Font(font="Consolas", size=16)
        tab_size: int = 4
        
        Editor.text_writer = tk.Text(
            master=Editor.frame, font=text_font, borderwidth=0,
            fg='white', background='#2E302F', wrap='none', padx=5, pady=5, 
            tabs=text_font.measure(' ' * tab_size)
        )

        Editor.text_writer.pack(side="left", fill="both", expand=True)

        # Scrollbar
        Editor.text_scroll = tk.Scrollbar(
            Editor.frame, orient="vertical", command=Editor.text_writer.yview,
            bg='#4A4A4A'
        )
        Editor.text_scroll.pack(side="right", fill="y")

        # Configures the text source to extend the scrollbar
        Editor.text_writer.config(yscrollcommand=Editor.text_scroll.set)
        Editor.text_writer.focus()

    @staticmethod
    def load_keybinds():
        """Load keybinds"""
        from src.main import App
        import src.functions.undo_redo as undo_redo
    
        if Editor.program:
            # Keybinds
            Editor.program.bind('<Control-Shift-S>', file_util.SaveFileAs.save)
            Editor.program.bind('<Control-Shift-O>', file_util.LoadFromFile.load)
            Editor.program.bind('<Control-s>', file_util.SaveCurrentFile.save)
            
            Editor.program.bind('<Control-z>', undo_redo.Undo.main)
            Editor.program.bind('<F9>', run_file.run_async)
            
            Editor.program.protocol("WM_DELETE_WINDOW", App.shutdown)

            # Editor.program.bind('<Destroy>', App.shutdown)
