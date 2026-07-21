from mazegen import Maze
from mlx import Mlx


def renderer(maze: Maze):
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    CELL_SIZE = 20
    WIDTH = maze.width * CELL_SIZE
    HEIGHT = maze.height * CELL_SIZE
    win_ptr = mlx.mlx_new_window(mlx_ptr, WIDTH, HEIGHT, "A-Maze-ing")
    img_ptr = mlx.mlx_new_image(mlx_ptr, WIDTH, HEIGHT)
    data, bpp, size_line, endian = mlx.mlx_get_data_addr(img_ptr)
    bytes_per_pixel = bpp // 8

    def put_pixel(x: int, y: int, color: int) -> None:
        offset = y * size_line + x * bytes_per_pixel
        pixel_end = offset + bytes_per_pixel
        data[offset:pixel_end] = color.to_bytes(bytes_per_pixel,
                                                byteorder="little")

    def render(param) -> None:
        mlx.mlx_sync(mlx_ptr, mlx.SYNC_IMAGE_WRITABLE, img_ptr)
        for row in maze.grid:
            for cell in row:
                if (cell.pos[0] == 0 or cell.pos[1] == 0 or
                        cell.pos[0] == (maze.width - 1) or
                        cell.pos[1] == (maze.height - 1)):
                    color = int("0xFFFFF200", 16)
                else:
                    color = int("0xFF000000", 16)
                px, py = cell.pos[0] * CELL_SIZE, cell.pos[1] * CELL_SIZE
                for dx in range(CELL_SIZE):
                    for dy in range(CELL_SIZE):
                        put_pixel(px + dx, py + dy, color)
        mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
        mlx.mlx_sync(mlx_ptr, mlx.SYNC_WIN_FLUSH, win_ptr)

    def key_press(keycode: int, param) -> None:
        if keycode == 65307:
            mlx.mlx_loop_exit(mlx_ptr)

    mlx.mlx_loop_hook(mlx_ptr, render, None)
    mlx.mlx_key_hook(win_ptr, key_press, None)
    mlx.mlx_loop(mlx_ptr)
