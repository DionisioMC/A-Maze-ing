from typing import Any
from random import Random, randint
from .cell import Cell


class MazeException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class MazeGenerator:
    def __init__(self, settings: dict[str, Any]):
        self.width = settings["WIDTH"]
        self.height = settings["HEIGHT"]
        self.entry = settings["ENTRY"]
        self.exit = settings["EXIT"]
        if not settings["SEED"]:
            self.seed = randint(0, 9999999)
        else:
            self.seed = settings["SEED"]
        self.output_file = settings["OUTPUT_FILE"]
        self.perfect = settings["PERFECT"]
        self.grid = self.set_grid()
        self.rndm = Random(self.seed)
        if self.width <= 10 or self.height <= 10:
            self.mask_42: list[tuple[int, int]] = []
            print("Maze not big enough for 42 mask")
        else:
            self.mask_42 = self.get_42()

    def generate_maze(self) -> None:
        try:
            if self.entry in self.mask_42:
                raise MazeException("Entry is in the 42 mask!")
            if self.exit in self.mask_42:
                raise MazeException("Exit is in the 42 mask!")
            visited: list[tuple[int, int]] = []
            for coord in self.mask_42:
                visited.append(coord)
            maze_stack: list[tuple[int, int]] = []
            visited.append(self.entry)
            maze_stack.append(self.entry)
            while maze_stack:
                cy, cx = maze_stack[-1]
                moves = [(1, 0, 'south'), (-1, 0, 'north'), (0, 1, 'east'),
                         (0, -1, 'west')]
                neighbours: list[tuple[int, int, str]] = []
                for my, mx, direction in moves:
                    ny, nx = (cy + my, cx + mx)
                    if (
                        (ny, nx) not in visited
                        and 0 <= ny < self.height
                        and 0 <= nx < self.width
                       ):
                        neighbours.append((ny, nx, direction))
                if neighbours:
                    ny, nx, direction = self.rndm.choice(neighbours)
                    self.break_walls((cy, cx), (ny, nx), direction)
                    visited.append((ny, nx))
                    maze_stack.append((ny, nx))
                else:
                    maze_stack.pop()
            if self.perfect is False:
                self.generate_imperfect()
        except Exception as e:
            print(f"Maze generation error: {e}")

    def generate_imperfect(self) -> None:
        rem_quant = self.height * self.width // 10
        while rem_quant:
            cy = self.rndm.randint(0, self.height - 1)
            cx = self.rndm.randint(0, self.width - 2)
            if ((cy, cx) not in self.mask_42 and
                (cy, cx + 1) not in self.mask_42 and
                    self.grid[cy][cx].east == 1):
                self.break_walls((cy, cx), (cy, cx + 1), 'east')
                rem_quant -= 1

    def set_grid(self) -> list[list[Cell]]:
        grid = [[Cell(1, 1, 1, 1, (y, x)) for x in range(self.width)]
                for y in range(self.height)]
        return grid

    def get_42(self) -> list[tuple[int, int]]:
        center = (self.height // 2, self.width // 2)
        mask_coords = [
            (-2, -3), (-1, -3), (0, -3), (0, -2), (0, -1), (1, -1), (2, -1),
            (-2, 1), (-2, 2), (-2, 3), (-1, 3), (0, 3), (0, 2), (0, 1),
            (1, 1), (2, 1), (2, 2), (2, 3)
            ]
        mask_42 = [(center[0] + coord[0], center[1] + coord[1])
                   for coord in mask_coords]
        return mask_42

    def break_walls(self, curr: tuple[int, int], next: tuple[int, int],
                    direction: str):
        cy, cx = curr
        ny, nx = next
        if direction == 'north':
            self.grid[cy][cx].north = 0
            self.grid[ny][nx].south = 0
        elif direction == 'south':
            self.grid[cy][cx].south = 0
            self.grid[ny][nx].north = 0
        elif direction == 'east':
            self.grid[cy][cx].east = 0
            self.grid[ny][nx].west = 0
        else:
            self.grid[cy][cx].west = 0
            self.grid[ny][nx].east = 0
