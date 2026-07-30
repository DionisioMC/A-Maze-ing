from sys import argv, exit
from typing import Any
from config_parse import config_parse
from mazegen import MazeGenerator, RecursiveBacktracker, Kruskal, Prim
from maze_solver import maze_solver
from renderer import renderer


def select_mazeGenerator(settings: dict[str, Any]) -> MazeGenerator:
    mazeGenerator: MazeGenerator
    if (not settings["ALGORITHM"] or settings["ALGORITHM"] ==
            "RecursiveBacktracker"):
        mazeGenerator = RecursiveBacktracker(settings)
    elif settings["ALGORITHM"] == "Prim":
        mazeGenerator = Prim(settings)
    elif settings["ALGORITHM"] == "Kruskal":
        mazeGenerator = Kruskal(settings)
    return mazeGenerator


def main() -> None:
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
            print(f"Error opening file {argv[1]}: {e}")
            exit(1)
    else:
        print("Usage: python3 a_maze_ing.py config.txt")


if __name__ == "__main__":
    main()
