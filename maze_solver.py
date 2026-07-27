from mazegen import Maze


def maze_solver(maze: Maze) -> str:
    entry = maze.entry
    exit = maze.exit
    queue: list[tuple[int, int]] = []
    queue.append(entry)
    visited: set[tuple[int, int]] = set()
    visited.add(entry)
    came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
    while len(queue):
        current_pos = queue.pop(0)
        if current_pos == exit:
            break
        current_cell = maze.grid[current_pos[1]][current_pos[0]]
        for (direction, dx, dy) in [("north", 0, -1), ("east", 1, 0),
                                    ("south", 0, 1), ("west", -1, 0)]:
            if not getattr(current_cell, direction):
                neigh_pos = (current_pos[0] + dx, current_pos[1] + dy)
                is_next = (((neigh_pos[0] >= 0 and
                             neigh_pos[0] < maze.width) and
                            (neigh_pos[1] >= 0 and
                             neigh_pos[1] < maze.height)))
                if is_next and neigh_pos not in visited:
                    visited.add(neigh_pos)
                    came_from[(neigh_pos)] = (current_pos, direction)
                    queue.append(neigh_pos)
    path = ""
    pos = exit
    while pos != entry:
        prev_pos, direction = came_from[pos]
        path = direction[0].capitalize() + path
        pos = prev_pos
    return path
