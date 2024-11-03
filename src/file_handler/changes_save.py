from json import load, dump


class SaveChanges:
    """Manage userdata (file only) to edit last changes & files editing before."""
    data_path: str = "data/userdata.json"

    @staticmethod
    def push(file_path: str, priority: int | None = None) -> None:
        """Add a file to the data"""
        # Opens & load user data
        data: dict = {}
        final_priority: int = 0 # file priority

        with open(SaveChanges.data_path, "r") as data_file:
            data = load(data_file)

        # Writes data in userdata
        opened_files: list[tuple[str, int]] = data["opened_files"]
        amount_files: int = len(opened_files)

        final_priority = (priority) or (amount_files > 0 and opened_files[amount_files][1] + 1) or (1)

        opened_files.append((file_path, final_priority))

        with open(SaveChanges.data_path, "w") as data_file:
            dump(data, data_file)

        # Add to queue|
        # queue.append((file_path, final_priority))
        # queue.sort(key=lambda file: (-file[1], queue.index(file)))

    @staticmethod
    # def pop(file_path: str) -> None:
    #     """Pop a file from data."""
    #     for index, file_info in enumerate(EditingFiles.stack):
    #         if file_info[0] == file_path:
    #             EditingFiles.stack.pop(index)
    #             break

    @staticmethod
    def search(file_path: str) -> tuple[str, int] | None:
        """Search for a file on editing list"""
        with open(SaveChanges.data_path, "r") as data_file:
            data = load(data_file)
            for file_info in data["opened_files"]:
                if file_info[0] == file_path:
                    return file_info
        return None

    @staticmethod
    def peek() -> tuple[str, int] | None:
        """Peeks the file with highest priority. (Also the current file)"""
        with open(SaveChanges.data_path, "r") as data_file:
            data = load(data_file)

            if len(data["opened_files"]) > 0:
                for file_info in data["opened_files"]:
                    if file_info[1] == 1:
                        return file_info

            return None
