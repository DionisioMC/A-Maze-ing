from sys import argv
from typing import Any
from config_parse import config_parse
from mazegen import MazeGenerator
from renderer import renderer


def main() -> None:
    if len(argv) == 2:
        with open(argv[1]) as file:
            settings: dict[str, Any] = config_parse(list(filter(lambda line:
                                                                line and not
                                                                line.
                                                                startswith(
                                                                    "#"),
                                                                file.read().
                                                                split("\n"))))
            mazeGenerator = MazeGenerator(settings)
            maze = mazeGenerator.generate_maze()
            renderer(maze)
    else:
        print("Usage: python3 a_maze_ing.py config.txt")


if __name__ == "__main__":
    main()
