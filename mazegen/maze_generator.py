from typing import Any
from random import seed
from .cell import Cell
from .maze import Maze


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

    def generate_maze(self) -> Maze:
        try:
            if self.seed:
                seed(self.seed)
            maze = Maze(self.width, self.height, self.entry, self.exit)
            for y in range(maze.height):
                row: list[Cell] = []
                for x in range(maze.width):
                    if y == 0:
                        if x == maze.width - 1:
                            row.append(Cell(1, 1, 0, 0, (x, y)))
                            continue
                        elif x == 0:
                            row.append(Cell(1, 0, 0, 1, (x, y)))
                            continue
                        row.append(Cell(1, 0, 0, 0, (x, y)))
                    elif y == maze.height - 1:
                        if x == self.width - 1:
                            row.append(Cell(0, 1, 1, 0, (x, y)))
                            continue
                        elif x == 0:
                            row.append(Cell(0, 0, 1, 1, (x, y)))
                            continue
                        row.append(Cell(0, 0, 1, 0, (x, y)))
                    elif x == 0:
                        row.append(Cell(0, 0, 0, 1, (x, y)))
                    elif x == maze.width - 1:
                        row.append(Cell(0, 1, 0, 0, (x, y)))
                    else:
                        row.append(Cell(0, 0, 0, 0, (x, y)))
                maze.grid.append(row)
        except Exception as e:
            print(f"Maze generation error: {e}")
        return maze
