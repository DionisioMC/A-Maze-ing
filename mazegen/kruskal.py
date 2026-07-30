from .maze_generator import MazeGenerator


class Kruskal(MazeGenerator):
    def generate_maze(self) -> None:
        try:
            groups: dict[tuple[int, int], tuple[int, int]] = {}
            walls: list[tuple[tuple[int, int], tuple[int, int], str]] = []
            for y in range(self.height):
                for x in range(self.width):
                    if (y, x) in self.mask_42:
                        continue
                    groups[(y, x)] = (y, x)
                    if (x < self.width - 1
                        and (y, x + 1) not in self.mask_42):
                        walls.append(((y, x), (y, x + 1), 'east'))
                    if (y < self.height - 1
                        and (y + 1, x) not in self.mask_42):
                        walls.append(((y, x), (y + 1, x), 'south'))

            def find(cell: tuple[int, int]) -> tuple[int, int]:
                if groups[cell] != cell:
                    groups[cell] = find(groups[cell])
                return groups[cell]

            def union(cell_1: tuple[int, int], 
                      cell_2: tuple[int, int]) -> bool:
                group_1 = find(cell_1)
                group_2 = find(cell_2)
                if group_1 != group_2:
                    groups[group_2] = group_1
                    return True
                return False

            self.rndm.shuffle(walls)
            while walls:
                cell_1, cell_2, direction = walls.pop()
                if union(cell_1, cell_2):
                    self.break_walls(cell_1, cell_2, direction)
            if self.perfect is False:
                self.generate_imperfect()
        except Exception as e:
            print(f"Maze generation error: {e}")