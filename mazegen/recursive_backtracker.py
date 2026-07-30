from .maze_generator import MazeGenerator


class RecursiveBacktracker(MazeGenerator):
    def generate_maze(self) -> None:
        try:
            visited = self.mask_42.copy()
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
            raise Exception(f"Maze generation error: {e}")
