from mazegen import MazeGenerator
from mlx import Mlx
from maze_solver import maze_solver


def renderer(maze: MazeGenerator, path: str):
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    has_path: bool = True
    i: int = -1
    CELL_SIZE = 20
    WALL_THICKNESS = 3
    BLOCK_SIZE = CELL_SIZE + WALL_THICKNESS
    WALL_COLOR = int("0xFFFFF200", 16)
    FT_COLOR = int("0xFFFFF200", 16)
    ENTRY_COLOR = int("0xFF3BB143", 16)
    EXIT_COLOR = int("0xFFFF2400", 16)
    PATH_COLOR = int("0xFF2400FF", 16)
    BG_COLOR = int("0xFF000000", 16)
    ALT_COLORS = [int("0xFFFFF200", 16), int("0xFFFFFFFF", 16),
                  int("0xFFFF6E00", 16)]
    WIDTH = maze.width * CELL_SIZE + (maze.width + 1) * WALL_THICKNESS
    HEIGHT = maze.height * CELL_SIZE + (maze.height + 1) * WALL_THICKNESS
    PADDING = 40
    win_ptr = mlx.mlx_new_window(mlx_ptr,
                                 (WIDTH + (PADDING * 2)),
                                 (HEIGHT + (PADDING * 2)),
                                 "A-Maze-ing")
    img_ptr = mlx.mlx_new_image(mlx_ptr,
                                (WIDTH + (PADDING * 2)),
                                (HEIGHT + (PADDING * 2)))
    data, bpp, size_line, endian = mlx.mlx_get_data_addr(img_ptr)
    bytes_per_pixel = bpp // 8

    def put_pixel(x: int, y: int, color: int) -> None:
        offset = y * size_line + x * bytes_per_pixel
        pixel_end = offset + bytes_per_pixel
        data[offset:pixel_end] = color.to_bytes(bytes_per_pixel,
                                                byteorder="little")

    def cell_origin(cell) -> tuple[int, int]:
        py = (cell.pos[0] * (CELL_SIZE + WALL_THICKNESS) + WALL_THICKNESS
              + PADDING)
        px = (cell.pos[1] * (CELL_SIZE + WALL_THICKNESS) + WALL_THICKNESS
              + PADDING)
        return (py, px)

    def render(param) -> None:
        for row in maze.grid:
            for cell in row:
                py, px = cell_origin(cell)
                for dx in range(CELL_SIZE + (WALL_THICKNESS * 2)):
                    for dy in range(CELL_SIZE + (WALL_THICKNESS * 2)):
                        put_pixel(px + dx, py + dy, BG_COLOR)
        if has_path:
            path = maze_solver(maze)
            path_cell = maze.grid[maze.entry[0]][maze.entry[1]]
            for direction in path:
                next_y: int = path_cell.pos[0]
                next_x: int = path_cell.pos[1]
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
                    py, px = cell_origin(path_cell)
                    for dx in range(CELL_SIZE):
                        for dy in range(CELL_SIZE):
                            put_pixel(px + dx, py + dy, PATH_COLOR)

        for row in maze.grid:
            for cell in row:
                py, px = cell_origin(cell)

                if cell.pos == maze.entry:
                    for dx in range(CELL_SIZE):
                        for dy in range(CELL_SIZE):
                            put_pixel(px + dx, py + dy, ENTRY_COLOR)
                elif cell.pos == maze.exit:
                    for dx in range(CELL_SIZE):
                        for dy in range(CELL_SIZE):
                            put_pixel(px + dx, py + dy, EXIT_COLOR)

                if cell.get_hex() == "F":
                    for dx in range(BLOCK_SIZE):
                        for dy in range(BLOCK_SIZE):
                            put_pixel(px + dx, py + dy, FT_COLOR)
                else:
                    if cell.north:
                        for dx in range(BLOCK_SIZE):
                            for dy in range(WALL_THICKNESS):
                                put_pixel(px + dx, py - WALL_THICKNESS + dy,
                                          WALL_COLOR)
                    if cell.south:
                        for dx in range(-WALL_THICKNESS, CELL_SIZE):
                            for dy in range(WALL_THICKNESS):
                                put_pixel(px + dx, py + CELL_SIZE + dy,
                                          WALL_COLOR)
                    if cell.west:
                        for dx in range(WALL_THICKNESS):
                            for dy in range(-WALL_THICKNESS, CELL_SIZE):
                                put_pixel(px - WALL_THICKNESS + dx, py + dy,
                                          WALL_COLOR)
                    if cell.east:
                        for dx in range(WALL_THICKNESS):
                            for dy in range(BLOCK_SIZE):
                                put_pixel(px + CELL_SIZE + dx, py + dy,
                                          WALL_COLOR)
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

    def key_press(keycode: int, param) -> None:
        if keycode == 49:
            mlx.mlx_loop_exit(mlx_ptr)
        elif keycode == 50:
            maze.grid = maze.set_grid()
            maze.generate_maze()
        elif keycode == 51:
            nonlocal has_path
            has_path = not has_path
        elif keycode == 52:
            nonlocal i
            nonlocal WALL_COLOR
            i += 1
            if i == len(ALT_COLORS):
                i = 0
            WALL_COLOR = ALT_COLORS[i]
        elif keycode == 53:
            pass

    mlx.mlx_loop_hook(mlx_ptr, render, None)
    mlx.mlx_key_hook(win_ptr, key_press, None)
    mlx.mlx_loop(mlx_ptr)
