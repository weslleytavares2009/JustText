import asyncio
import threading
from tkinter import Event, messagebox
from src.file_handler.changes_save import SaveChanges
from json import load

# Global variable for the asyncio event loop
asyncio_loop = None

def start_loop():
    """Function to run the asyncio event loop in a separate thread."""
    global asyncio_loop
    asyncio_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(asyncio_loop)
    asyncio_loop.run_forever()

# Start the asyncio loop in a new thread
threading.Thread(target=start_loop, daemon=True).start()

async def run_command(command: str) -> tuple[str, str]:
    """Execute a shell command asynchronously and return output and errors."""
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

def handle_output(stdout: str, stderr: str) -> None:
    """Print the output and errors from command execution."""
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

async def execute_file(file_path: str) -> None:
    """Execute the file based on its extension."""
    file_extension: str = file_path.split('.')[-1]
    
    match file_extension:  # Get the file extension
        case 'py':
            stdout, stderr = await run_command(f"py -u {file_path}")
            handle_output(stdout, stderr)
        case 'java':
            # Compile and execute the Java file
            compile_stdout, compile_stderr = await run_command(f"javac {file_path}")
            handle_output(compile_stdout, compile_stderr)

            execute_stdout, execute_stderr = await run_command(f"java {file_path}")  # Exclude .java extension
            handle_output(execute_stdout, execute_stderr)
        case _:
            messagebox.showwarning(
                "Unsupported file type", 
                f"JustText doesn't have built-in support for '.{file_extension}' files."
            )

async def run_files(opened_files: list[tuple[str, int]]) -> None:
    """Run the files based on their priority and extension."""
    for file_info in opened_files:
        file_path: str = file_info[0]
        file_priority: int = file_info[1]

        if file_priority == 1:
            await execute_file(file_path)

async def load_opened_files() -> list[tuple[str, int]]:
    """Load the opened files from the JSON data."""
    with open(SaveChanges.data_path, "r") as data_file:
        content = load(data_file)
        return content["opened_files"]

async def run() -> None:
    """Main async function to execute files."""
    opened_files = await load_opened_files()
    await run_files(opened_files)

def run_async(event: Event):
    """Safely run the coroutine in the asyncio event loop."""
    if asyncio_loop is not None:
        asyncio.run_coroutine_threadsafe(run(), asyncio_loop)
