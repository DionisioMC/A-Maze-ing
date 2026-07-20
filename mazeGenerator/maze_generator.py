from typing import Any


class MazeException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class MazeGenerator:
    def __init__(self, settings: dict[str, Any]):
        self.width = settings["WIDTH"]
        self.height = settings["HEIGHT"]
        self.entry = settings["ENTRY"]
        self.exit = settings["EXIT"]
        self.seed = settings["SEED"]
        self.output_file = settings["OUTPUT_FILE"]
        self.perfect = settings["PERFECT"]

    def generate_maze(self):
        pass
