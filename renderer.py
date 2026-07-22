from mazegen import Maze
from mlx import Mlx


def renderer(maze: Maze):
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    CELL_SIZE = 20
    WALL_THICKNESS = 3
    WALL_COLOR = int("0xFFFFF200", 16)
    ENTRY_COLOR = int("0xFF2400FF", 16)
    EXIT_COLOR = int("0xFFFF2400", 16)
    WIDTH = maze.width * CELL_SIZE
    HEIGHT = maze.height * CELL_SIZE
    PADDING = 40
    win_ptr = mlx.mlx_new_window(mlx_ptr, WIDTH + (PADDING * 2),
                                 HEIGHT + (PADDING * 2), "A-Maze-ing")
    img_ptr = mlx.mlx_new_image(mlx_ptr, WIDTH + (PADDING * 2),
                                HEIGHT + (PADDING * 2))
    data, bpp, size_line, endian = mlx.mlx_get_data_addr(img_ptr)
    bytes_per_pixel = bpp // 8

    def put_pixel(x: int, y: int, color: int) -> None:
        offset = y * size_line + x * bytes_per_pixel
        pixel_end = offset + bytes_per_pixel
        data[offset:pixel_end] = color.to_bytes(bytes_per_pixel,
                                                byteorder="little")

    def render(param) -> None:
        for row in maze.grid:
            for cell in row:
                px, py = (cell.pos[0] * CELL_SIZE + PADDING,
                          cell.pos[1] * CELL_SIZE + PADDING)

                for dx in range(CELL_SIZE):
                    for dy in range(CELL_SIZE):
                        if cell.pos == maze.entry:
                            put_pixel(px + dx, py + dy, ENTRY_COLOR)
                        elif cell.pos == maze.exit:
                            put_pixel(px + dx, py + dy, EXIT_COLOR)

                if cell.north:
                    for dx in range(CELL_SIZE):
                        for dy in range(WALL_THICKNESS):
                            put_pixel(px + dx, py + dy, WALL_COLOR)

                if cell.south:
                    for dx in range(CELL_SIZE):
                        for dy in range(CELL_SIZE - WALL_THICKNESS, CELL_SIZE):
                            put_pixel(px + dx, py + dy, WALL_COLOR)

                if cell.west:
                    for dx in range(WALL_THICKNESS):
                        for dy in range(CELL_SIZE):
                            put_pixel(px + dx, py + dy, WALL_COLOR)

                if cell.east:
                    for dx in range(CELL_SIZE - WALL_THICKNESS, CELL_SIZE):
                        for dy in range(CELL_SIZE):
                            put_pixel(px + dx, py + dy, WALL_COLOR)
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

    def key_press(keycode: int, param) -> None:
        if keycode == 65307:
            mlx.mlx_loop_exit(mlx_ptr)

    mlx.mlx_loop_hook(mlx_ptr, render, None)
    mlx.mlx_key_hook(win_ptr, key_press, None)
    mlx.mlx_loop(mlx_ptr)
