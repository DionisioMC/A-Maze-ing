from .maze_generator import MazeGenerator


class Prim(MazeGenerator):
    def generate_maze(self) -> None:
        try:
            visited = self.mask_42.copy()
            frontier: list[tuple[int, int]] = []
            visited.append(self.entry)
            self.append_neighbours(self.entry, visited, frontier)
            while frontier:
                cy, cx = self.rndm.choice(frontier)
                frontier.remove((cy, cx))
                moves = [(1, 0, 'south'), (-1, 0, 'north'), (0, 1, 'east'),
                         (0, -1, 'west')]
                possible_breaks: list[tuple[int, int, str]] = []
                for my, mx, direction in moves:
                    ny, nx = (cy + my, cx + mx)
                    if (ny, nx) in visited and (ny, nx) not in self.mask_42:
                        possible_breaks.append((ny, nx, direction))
                if possible_breaks:
                    ny, nx, direction = self.rndm.choice(possible_breaks)
                    self.break_walls((cy, cx), (ny, nx), direction)
                    visited.append((cy, cx))
                    self.append_neighbours((cy, cx), visited, frontier)
            if self.perfect is False:
                self.generate_imperfect()
        except Exception as e:
            print(f"Maze generation error: {e}")

    def append_neighbours(self, cell: tuple[int, int],
                          visited: list[tuple[int, int]],
                          frontier: list[tuple[int, int]]) -> None:
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        cy, cx = cell
        for my, mx in moves:
            ny, nx = (cy + my, cx + mx)
            if (
                (ny, nx) not in visited
                and (ny, nx) not in frontier
                and 0 <= ny < self.height
                and 0 <= nx < self.width
                    ):
                frontier.append((ny, nx))
