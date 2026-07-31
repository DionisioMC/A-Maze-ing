from sys import argv, exit
from typing import Any
from mazegen import (MazeGenerator, config_parse, maze_solver,
                     select_mazeGenerator, renderer)


def main() -> None:
    """Entry point: read the config file passed as a command-line
    argument, generate the maze, solve it and render the result."""
    if len(argv) == 2:
        try:
            with open(argv[1]) as file:
                settings: dict[str, Any] = config_parse(
                    list(filter(lambda line: line and not line.startswith("#"),
                                file.read().split("\n"))))
                maze: MazeGenerator = select_mazeGenerator(settings)
                maze.generate_maze()
                path = maze_solver(maze)
                renderer(maze, path)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
    else:
        print("Usage: python3 a_maze_ing.py config.txt")


if __name__ == "__main__":
    main()
