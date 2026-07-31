from .maze_generator import MazeGenerator


def maze_solver(maze: MazeGenerator) -> str:
    """Find the shortest path from the maze's entry to its exit using
    breadth-first search, write the maze (as hex-encoded cells),
    entry/exit coordinates and the solution path to the output file,
    and return the path as a string of direction letters (N/E/S/W)."""
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
        current_cell = maze.grid[current_pos[0]][current_pos[1]]
        for (direction, dy, dx) in [("north", -1, 0), ("east", 0, 1),
                                    ("south", 1, 0), ("west", 0, -1)]:
            if not getattr(current_cell, direction):
                neigh_pos = (current_pos[0] + dy, current_pos[1] + dx)
                is_next = (((neigh_pos[0] >= 0 and
                             neigh_pos[0] < maze.height) and
                            (neigh_pos[1] >= 0 and
                             neigh_pos[1] < maze.width)))
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
    try:
        with open(maze.output_file, 'w') as file:
            for row in maze.grid:
                for cell in row:
                    file.write(cell.get_hex())
                file.write("\n")
            file.write(f"\n{maze.entry[0]},{maze.entry[1]}\n")
            file.write(f"{maze.exit[0]},{maze.exit[1]}\n")
            file.write(f"{path}\n")
    except Exception as e:
        raise Exception(f"Error opening output file: {e}")
    return path
