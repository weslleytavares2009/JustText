from src.editor_style.editor import Editor
from src.file_handler.changes_save import SaveChanges
from tkinter import Event, END

historic: list[str] = []
holding_ctrl: bool = False

def monitore_release(event: Event) -> None:
    released_key: str = event.char or event.keysym
    holding_ctrl = released_key == "Control_L"

def add_to_historic(event: Event) -> None:
    # Get key pressed
    pressed_key: str = event.char or event.keysym or " "
    holding_ctrl = pressed_key == "Control_L"
    
    # Add to modified files
    if (pressed_key != "Right" and pressed_key != "Left"
            and pressed_key != "Up" and pressed_key != "Down"):
        
        # Add to editing file list
        current_file: tuple[str, int] | None = SaveChanges.peek()
        if not holding_ctrl and current_file and not current_file[0] in Editor.modified_files:
            Editor.modified_files.append(current_file[0])
    
        if not holding_ctrl:
            # Get cursor position on "line.column" format
            cursor: str = Editor.text_writer.index("insert")
            text_to_cursor: list[str] = Editor.text_writer.get("1.0", cursor).split("\n")
            line, column = len(text_to_cursor), len(text_to_cursor[-1]) + 1

            # Get the last phrase typed
            last_phrase: str = text_to_cursor[-1].split(" ")[-1]
            current_text: str = Editor.text_writer.get("1.0", "end-1c")
            _UndoRedoManager.add_action(last_phrase, line, column)
            _UndoRedoManager.current_text = current_text
    
        
Editor.text_writer.bind('<KeyPress>', add_to_historic)
Editor.text_writer.bind('<KeyRelease>', monitore_release)

class _UndoRedoManager:
    """Control Undo & Redo history implementing a Stack structure"""
    undo_stack = []  # Stores tuples: (word, line, column)
    redo_stack = []
    current_text = ""  # Full text representation

    @staticmethod
    def add_action(word: str, line: int, column: int) -> None:
        """Add a new action to the undo stack and clear the redo stack"""
        _UndoRedoManager.undo_stack.append((word, line, column))
        print(_UndoRedoManager.undo_stack)

    @staticmethod
    def undo() -> None:
        """Remove last step (Undo)"""
        if not _UndoRedoManager.undo_stack:
            return  # No action to undo
        
        # Pop the last action and push to redo stack
        last_word, line, column = _UndoRedoManager.undo_stack.pop()
        _UndoRedoManager.redo_stack.append((last_word, line, column))
        
        # Remove the word from current_text based on line and column
        lines = _UndoRedoManager.current_text.split('\n')
        if 0 <= line - 1 < len(lines):
            line_content = lines[line - 1]
            new_line_content = line_content[:column - 1] + line_content[column - 1:].rsplit(last_word, 1)[0]
            lines[line - 1] = new_line_content.rstrip()
        
        _UndoRedoManager.current_text = '\n'.join(lines)

    @staticmethod
    def redo() -> None:
        """Restore last step (Redo)"""
        if not _UndoRedoManager.redo_stack:
            return  # No action to redo
        
        # Pop the last action and push to undo stack
        word, line, column = _UndoRedoManager.redo_stack.pop()
        _UndoRedoManager.undo_stack.append((word, line, column))
        
        # Add the word back into current_text based on line and column
        lines = _UndoRedoManager.current_text.split('\n')
        if 0 <= line - 1 < len(lines):
            line_content = lines[line - 1]
            new_line_content = line_content[:column - 1] + word + line_content[column - 1:]
            lines[line - 1] = new_line_content
        
        _UndoRedoManager.current_text = '\n'.join(lines)

class Undo:
    def main(event: Event):
        _UndoRedoManager.undo()
        Editor.text_writer.delete("1.0", END)
        Editor.text_writer.insert(END, _UndoRedoManager.current_text)
        print(_UndoRedoManager.undo_stack, _UndoRedoManager.redo_stack)
