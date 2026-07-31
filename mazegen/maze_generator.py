from typing import Any
from random import Random, randint
from .cell import Cell
from abc import ABC, abstractmethod


class MazeException(Exception):
    """Custom exception used to signal maze generation/configuration
    errors (e.g. entry or exit placed inside the forbidden '42' mask)."""

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)


class MazeGenerator(ABC):
    """Abstract base class for maze generation algorithms. Sets up the
    grid, seed, entry/exit points and the forbidden '42' mask, and
    provides shared helpers used by concrete generator subclasses."""

    def __init__(self, settings: dict[str, Any]):
        """Initialize the generator from a parsed settings dict: build
        the grid, resolve/record the RNG seed, and compute the '42'
        mask (raising MazeException if entry/exit fall inside it)."""
        self.width = settings["WIDTH"]
        self.height = settings["HEIGHT"]
        self.entry = settings["ENTRY"]
        self.exit = settings["EXIT"]
        if not settings["SEED"]:
            self.seed = randint(0, 9999999)
        else:
            self.seed = settings["SEED"]
        try:
            with open("seed_history.txt", "a") as file:
                file.write(f"{self.seed}\n")
        except Exception as e:
            raise Exception(f"Error writing to file seed_history.txt: {e}")
        self.output_file = settings["OUTPUT_FILE"]
        self.perfect = settings["PERFECT"]
        self.grid = self.set_grid()
        self.rndm = Random(self.seed)
        if self.width < 8 or self.height < 6:
            self.mask_42: list[tuple[int, int]] = []
            print("Maze not big enough for 42 mask")
        else:
            self.mask_42 = self.get_42()
        try:
            if self.entry in self.mask_42:
                raise MazeException("Entry is in the 42 mask!\n"
                                    f"Forbidden cells: {self.mask_42}")
            if self.exit in self.mask_42:
                raise MazeException("Exit is in the 42 mask!\n"
                                    f"Forbidden cells: {self.mask_42}")
        except Exception as e:
            raise Exception(f"Maze generation error: {e}")

    @abstractmethod
    def generate_maze(self) -> None:
        """Carve the maze passages into `self.grid`. Must be
        implemented by each concrete generation algorithm."""
        pass

    def generate_imperfect(self) -> None:
        """Turn a perfect maze into an imperfect one by randomly
        breaking extra east-facing walls (loops), skipping cells in
        the '42' mask, until roughly 10% of cells have been altered."""
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
        """Build and return a `height` x `width` grid of Cells with
        all four walls closed."""
        grid = [[Cell(1, 1, 1, 1, (y, x)) for x in range(self.width)]
                for y in range(self.height)]
        return grid

    def get_42(self) -> list[tuple[int, int]]:
        """Compute and return the list of grid coordinates forming the
        '42'-shaped mask of forbidden cells, centered on the grid."""
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
                    direction: str) -> None:
        """Open the wall between two adjacent cells `curr` and `next`
        in the given `direction`, clearing the matching wall on both
        cells so they become connected."""
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
