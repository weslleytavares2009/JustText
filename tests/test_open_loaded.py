import unittest
from src.main import App
from src.file_handler import file

class SimulateOpenFile(unittest.TestCase):
    def test_initialize(self):
        App()

    def test_load(self):
        file.LoadFromSave.load()

    def test_run(self):
        App.run()

if __name__ == "__main__":
    unittest.main()
