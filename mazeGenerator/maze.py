class Maze:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int]):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: list[list[int]] = []
