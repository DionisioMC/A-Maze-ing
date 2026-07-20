from sys import argv
from typing import Any
from config_parse import config_parse
from mazeGenerator import MazeGenerator


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
    else:
        print("Usage: python3 a_maze_ing.py config.txt")


if __name__ == "__main__":
    main()
