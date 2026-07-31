from .maze_generator import MazeGenerator
from .cell import Cell
from .mlx import Mlx
from .maze_solver import maze_solver
from random import randint, Random
from typing import Any


def renderer(maze: MazeGenerator, path: str) -> None:
    """Open an MLX window and interactively display the generated
    maze: draw cells, walls, entry/exit and an animated solution
    path, and handle key presses to cycle color themes, regenerate
    the maze with a new seed, toggle the solution path, or quit."""
    mlx: Mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    has_path: bool = True
    i: int = 0
    CELL_SIZE = 20
    WALL_THICKNESS = 3
    COLORS: list[dict[str, Any]] = [
        {
            "name": "Classic",
            "walls": int("0xFF202020", 16),
            "bg": int("0xFFF5F5F5", 16),
            "solution": int("0xFFFFD000", 16),
            "entry": int("0xFF00C853", 16),
            "exit": int("0xFFD50000", 16),
            "closed": int("0xFF90A4AE", 16),
        },
        {
            "name": "Neon",
            "walls": int("0xFF0D0D0D", 16),
            "bg": int("0xFF121212", 16),
            "solution": int("0xFFFFFF00", 16),
            "entry": int("0xFF00FF9C", 16),
            "exit": int("0xFFFF1744", 16),
            "closed": int("0xFF303030", 16),
        },
        {
            "name": "Ocean",
            "walls": int("0xFF003049", 16),
            "bg": int("0xFFEAF7FF", 16),
            "solution": int("0xFFFFC300", 16),
            "entry": int("0xFF00B4D8", 16),
            "exit": int("0xFFE63946", 16),
            "closed": int("0xFF90E0EF", 16),
        },
        {
            "name": "Forest",
            "walls": int("0xFF2D6A4F", 16),
            "bg": int("0xFFF1FAEE", 16),
            "solution": int("0xFFFFC300", 16),
            "entry": int("0xFF52B788", 16),
            "exit": int("0xFFD62828", 16),
            "closed": int("0xFF95D5B2", 16),
        },
        {
            "name": "Desert",
            "walls": int("0xFF6D4C41", 16),
            "bg": int("0xFFFFF8E1", 16),
            "solution": int("0xFFFFB703", 16),
            "entry": int("0xFF2A9D8F", 16),
            "exit": int("0xFFE63946", 16),
            "closed": int("0xFFDDB892", 16),
        },
        {
            "name": "Ice",
            "walls": int("0xFF274C77", 16),
            "bg": int("0xFFF8FCFF", 16),
            "solution": int("0xFFFFD60A", 16),
            "entry": int("0xFF48CAE4", 16),
            "exit": int("0xFFFF595E", 16),
            "closed": int("0xFFA9D6E5", 16),
        },
        {
            "name": "Lava",
            "walls": int("0xFF1B1B1B", 16),
            "bg": int("0xFF2B2D42", 16),
            "solution": int("0xFFFFC300", 16),
            "entry": int("0xFFFF6D00", 16),
            "exit": int("0xFFD00000", 16),
            "closed": int("0xFF5C677D", 16),
        },
        {
            "name": "Pastel",
            "walls": int("0xFF7B8FA1", 16),
            "bg": int("0xFFFFFBF2", 16),
            "solution": int("0xFFFFD166", 16),
            "entry": int("0xFF80ED99", 16),
            "exit": int("0xFFFF6B6B", 16),
            "closed": int("0xFFD6CCC2", 16),
        },
        {
            "name": "Cyberpunk",
            "walls": int("0xFF240046", 16),
            "bg": int("0xFF10002B", 16),
            "solution": int("0xFFFFEA00", 16),
            "entry": int("0xFF00F5D4", 16),
            "exit": int("0xFFFF006E", 16),
            "closed": int("0xFF5A189A", 16),
        },
        {
            "name": "Monochrome",
            "walls": int("0xFF000000", 16),
            "bg": int("0xFFFFFFFF", 16),
            "solution": int("0xFF808080", 16),
            "entry": int("0xFF00AA00", 16),
            "exit": int("0xFFAA0000", 16),
            "closed": int("0xFFBDBDBD", 16),
        },
        {
            "name": "42",
            "walls": int("0xFF000000", 16),
            "bg": int("0xFFF8F8F8", 16),
            "solution": int("0xFFFFFF00", 16),
            "entry": int("0xFF00BABC", 16),
            "exit": int("0xFFFF4D4D", 16),
            "closed": int("0xFF6C757D", 16),
        }
    ]
    CURR_COLORS = COLORS[i]
    BLOCK_SIZE = CELL_SIZE + WALL_THICKNESS
    WIDTH = maze.width * CELL_SIZE + (maze.width + 1) * WALL_THICKNESS
    HEIGHT = maze.height * CELL_SIZE + (maze.height + 1) * WALL_THICKNESS
    PADDING = 40
    path_cells: list[tuple[int, int]] = []
    animation_frame: int = 0
    FRAMES_PER_STEP: int = 1
    table_path = "mazegen/assets/table_horizontal.png"
    table, table_w, table_h = mlx.mlx_png_file_to_image(mlx_ptr,
                                                        table_path)
    if table_w <= (WIDTH + (PADDING * 2)):
        WIN_WIDTH = WIDTH + PADDING * 2
        WIN_HEIGHT = HEIGHT + PADDING * 2
        table_x = (WIN_WIDTH - table_w) // 2
        table_y = WIN_HEIGHT - table_h
    else:
        table_path = "mazegen/assets/table_vertical.png"
        table, table_w, table_h = mlx.mlx_png_file_to_image(mlx_ptr,
                                                            table_path)
        WIN_WIDTH = WIDTH + PADDING * 2 + table_w + PADDING
        WIN_HEIGHT = max(HEIGHT + PADDING * 2, table_h + PADDING * 2)
        table_x = WIDTH + PADDING * 2
        table_y = (WIN_HEIGHT - table_h) // 2
        table_path = "mazegen/assets/table_vertical"
    win_ptr = mlx.mlx_new_window(mlx_ptr, WIN_WIDTH, WIN_HEIGHT, "A-Maze-ing")
    img_ptr = mlx.mlx_new_image(mlx_ptr, WIN_WIDTH, WIN_HEIGHT)
    data, bpp, size_line, _ = mlx.mlx_get_data_addr(img_ptr)
    bytes_per_pixel = bpp // 8

    def put_pixel(x: int, y: int, color: int) -> None:
        """Write a single ARGB `color` value into the image buffer at
        pixel coordinates (x, y)."""
        offset = y * size_line + x * bytes_per_pixel
        pixel_end = offset + bytes_per_pixel
        data[offset:pixel_end] = color.to_bytes(bytes_per_pixel,
                                                byteorder="little")

    def cell_origin(cell: Cell) -> tuple[int, int]:
        """Return the (y, x) pixel coordinates of the top-left corner
        of `cell`'s drawable area on screen, including padding and
        wall-thickness offsets."""
        py = (cell.pos[0] * (CELL_SIZE + WALL_THICKNESS) + WALL_THICKNESS
              + PADDING)
        px = (cell.pos[1] * (CELL_SIZE + WALL_THICKNESS) + WALL_THICKNESS
              + PADDING)
        return (py, px)

    def animate_path() -> None:
        """Solve the maze and populate `path_cells` with the sequence
        of cell positions (excluding the exit) forming the solution
        path, to be revealed progressively during rendering."""
        solved_path = maze_solver(maze)
        path_cell = maze.grid[maze.entry[0]][maze.entry[1]]
        for direction in solved_path:
            next_y = path_cell.pos[0]
            next_x = path_cell.pos[1]
            if direction == "N":
                next_y -= 1
            elif direction == "E":
                next_x += 1
            elif direction == "S":
                next_y += 1
            elif direction == "W":
                next_x -= 1
            path_cell = maze.grid[next_y][next_x]
            if path_cell.pos != maze.exit:
                path_cells.append(path_cell.pos)

    animate_path()

    def render(param: Any) -> None:
        """MLX loop-hook callback: redraw the whole frame each tick —
        cell backgrounds, the progressively-animated solution path,
        entry/exit highlights, closed ('42' mask) cells and walls —
        then blit the image to the window."""
        nonlocal animation_frame
        for row in maze.grid:
            for cell in row:
                py, px = cell_origin(cell)
                for dx in range(CELL_SIZE + (WALL_THICKNESS * 2)):
                    for dy in range(CELL_SIZE + (WALL_THICKNESS * 2)):
                        put_pixel(px + dx, py + dy, CURR_COLORS["bg"])
        if has_path:
            cells_to_draw = animation_frame // FRAMES_PER_STEP
            for pos in path_cells[:cells_to_draw]:
                py, px = cell_origin(maze.grid[pos[0]][pos[1]])
                for dx in range(CELL_SIZE):
                    for dy in range(CELL_SIZE):
                        put_pixel(px + dx, py + dy, CURR_COLORS["solution"])
            if cells_to_draw < len(path_cells):
                animation_frame += 1

        for row in maze.grid:
            for cell in row:
                py, px = cell_origin(cell)

                if cell.pos == maze.entry:
                    for dx in range(CELL_SIZE):
                        for dy in range(CELL_SIZE):
                            put_pixel(px + dx, py + dy, CURR_COLORS["entry"])
                elif cell.pos == maze.exit:
                    for dx in range(CELL_SIZE):
                        for dy in range(CELL_SIZE):
                            put_pixel(px + dx, py + dy, CURR_COLORS["exit"])

                if cell.get_hex() == "F":
                    for dx in range(BLOCK_SIZE):
                        for dy in range(BLOCK_SIZE):
                            put_pixel(px + dx, py + dy, CURR_COLORS["closed"])
                else:
                    if cell.north:
                        for dx in range(BLOCK_SIZE):
                            for dy in range(WALL_THICKNESS):
                                put_pixel(px + dx, py - WALL_THICKNESS + dy,
                                          CURR_COLORS["walls"])
                    if cell.south:
                        for dx in range(-WALL_THICKNESS, CELL_SIZE):
                            for dy in range(WALL_THICKNESS):
                                put_pixel(px + dx, py + CELL_SIZE + dy,
                                          CURR_COLORS["walls"])
                    if cell.west:
                        for dx in range(WALL_THICKNESS):
                            for dy in range(-WALL_THICKNESS, CELL_SIZE):
                                put_pixel(px - WALL_THICKNESS + dx, py + dy,
                                          CURR_COLORS["walls"])
                    if cell.east:
                        for dx in range(WALL_THICKNESS):
                            for dy in range(BLOCK_SIZE):
                                put_pixel(px + CELL_SIZE + dx, py + dy,
                                          CURR_COLORS["walls"])
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

    def key_press(keycode: int, param: Any) -> None:
        """MLX key-hook callback handling user input: cycle to the
        next color theme (1), regenerate the maze with a fresh random
        seed (2), toggle the solution-path display (3), or exit the
        render loop (4)."""
        if keycode == 49:
            nonlocal i
            nonlocal CURR_COLORS
            i += 1
            if i == len(COLORS):
                i = 0
            CURR_COLORS = COLORS[i]
        elif keycode == 50:
            nonlocal animation_frame, path_cells
            animation_frame = 0
            path_cells = []
            maze.grid = maze.set_grid()
            maze.seed = randint(0, 9999999)
            maze.rndm = Random(maze.seed)
            try:
                with open("seed_history.txt", "a") as file:
                    file.write(f"{maze.seed}\n")
            except Exception as e:
                raise Exception(f"Error writing to file seed_history.txt: {e}")
            maze.generate_maze()
            animate_path()
        elif keycode == 51:
            nonlocal has_path
            has_path = not has_path
        elif keycode == 52:
            mlx.mlx_loop_exit(mlx_ptr)

    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, table, table_x, table_y)
    mlx.mlx_loop_hook(mlx_ptr, render, None)
    mlx.mlx_key_hook(win_ptr, key_press, None)
    mlx.mlx_loop(mlx_ptr)
