from tkinter import filedialog

class FileOpenDialog:
    @staticmethod
    def ask_open_file(initial_dir: str = None) -> str | None:
        """Ask the user to open a file. Returns the path of the file or None.
        Parameters:
        - initial_dir: The initial directory to open the file dialog (Optional)
        """
        return filedialog.askopenfilename(initialdir=initial_dir, 
                                          filetypes=[("All files", "*.*")])

class FileSaveDialog:
    @staticmethod
    def ask_save_file(default_ext: str = ".txt", initial_dir: str = None, 
                      initial_file: str = None) -> str | None:
        """Ask the user to save a file. Returns the path of the file or None.
        Parameters:
        - default_ext: The default extension of the file to be saved (Optional).
        - initial_dir: The initial directory to open the file dialog (Optional).
        - initial_file: The initial file to be selected. (Optional)"""
        return filedialog.asksaveasfilename(
            defaultextension=default_ext,
            filetypes=[("All files", "*.*")],
            initialdir=initial_dir,
            initialfile=initial_file
        )
