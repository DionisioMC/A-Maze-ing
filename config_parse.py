from typing import Any
from sys import exit


def parse_line(line: str) -> tuple[str, str]:
    setting, value = line.split("=")
    return setting.strip(), value.strip()


def config_parse(config: list[str]) -> dict[str, Any]:
    try:
        settings: dict[str, str] = dict(map(parse_line, config))
        keys: list[str] = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                           "OUTPUT_FILE", "PERFECT"]
        for key in keys:
            if not settings.get(key):
                raise ValueError(f"Key {key} is missing from configuration "
                                 "file")
        configuration: dict[str, Any] = {}
        configuration["WIDTH"] = int(settings["WIDTH"])
        configuration["HEIGHT"] = int(settings["HEIGHT"])
        configuration["ENTRY"] = tuple(map(lambda x: int(x),
                                           settings["ENTRY"].split(",")))
        configuration["EXIT"] = tuple(map(lambda x: int(x),
                                          settings["EXIT"].split(",")))
        if "SEED" not in settings.keys() or settings["SEED"] == "None":
            configuration["SEED"] = None
        elif settings["SEED"].isdigit():
            configuration["SEED"] = int(settings["SEED"])
        else:
            configuration["SEED"] = settings["SEED"]
        if "ALGORITHM" not in settings.keys():
            configuration["ALGORITHM"] = "RecursiveBacktracker"
        elif settings["ALGORITHM"] not in ["Prim", "RecursiveBacktracker",
                                           "Kruskal"]:
            raise ValueError("The specified Algorithm isn't valid")
        else:
            configuration["ALGORITHM"] = settings["ALGORITHM"]

        configuration["OUTPUT_FILE"] = settings["OUTPUT_FILE"]
        configuration["PERFECT"] = eval(settings["PERFECT"].capitalize())

        if configuration["WIDTH"] < 2 or configuration["HEIGHT"] < 2:
            raise ValueError("The maze has a minimum configuration of 2x2")
        if len(configuration["ENTRY"]) > 2:
            raise ValueError("Entry point should have 2 coordinates")
        if len(configuration["EXIT"]) > 2:
            raise ValueError("Exit point should have 2 coordinates")
        if ((configuration["ENTRY"][0] < 0 or
            configuration["ENTRY"][0] >= configuration["HEIGHT"]) or
            (configuration["ENTRY"][1] < 0 or
                configuration["ENTRY"][1] >= configuration["WIDTH"])):
            raise ValueError("Entry point is outside of the maze")
        if ((configuration["EXIT"][0] < 0 or
            configuration["EXIT"][0] >= configuration["HEIGHT"]) or
            (configuration["EXIT"][1] < 0 or
                configuration["EXIT"][1] >= configuration["WIDTH"])):
            raise ValueError("Exit point is outside of the maze")
        if configuration["ENTRY"] == configuration["EXIT"]:
            raise ValueError("Entry and exit set to the same coordenates")
    except ValueError as e:
        print(f"configuration file error: {e}")
        exit(1)
    return configuration
