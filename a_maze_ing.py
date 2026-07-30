from sys import argv
from typing import Any
from config_parse import config_parse
from mazegen import MazeGenerator, RecursiveBacktracker, Kruskal, Prim
from maze_solver import maze_solver
from renderer import renderer


def main() -> None:
    if len(argv) == 2:
        with open(argv[1]) as file:
            settings: dict[str, Any] = config_parse(
                list(filter(lambda line: line and not line.startswith("#"),
                     file.read().split("\n"))))
            maze: MazeGenerator = RecursiveBacktracker(settings)
            maze.generate_maze()
            path = maze_solver(maze)
            renderer(maze, path)
    else:
        print("Usage: python3 a_maze_ing.py config.txt")


if __name__ == "__main__":
    main()
