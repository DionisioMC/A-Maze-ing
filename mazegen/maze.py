from .cell import Cell


class Maze:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int]):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: list[list[Cell]] = []
        for y in range(0, self.height):
            row: list[Cell] = []
            for x in range(0, self.width):
                if y == 0:
                    if x == self.width - 1:
                        row.append(Cell(1, 1, 0, 0, (x, y)))
                        continue
                    elif x == 0:
                        row.append(Cell(1, 0, 0, 1, (x, y)))
                        continue
                    row.append(Cell(1, 0, 0, 0, (x, y)))
                elif y == self.height - 1:
                    if x == self.width - 1:
                        row.append(Cell(0, 1, 1, 0, (x, y)))
                        continue
                    elif x == 0:
                        row.append(Cell(0, 0, 1, 1, (x, y)))
                        continue
                    row.append(Cell(0, 0, 1, 0, (x, y)))
                elif x == 0:
                    row.append(Cell(0, 0, 0, 1, (x, y)))
                elif x == self.width - 1:
                    row.append(Cell(0, 1, 0, 0, (x, y)))
                else:
                    row.append(Cell(0, 0, 0, 0, (x, y)))
