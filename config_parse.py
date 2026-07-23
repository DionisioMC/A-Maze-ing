from typing import Any
from sys import exit


def parse_line(line: str) -> tuple[str, str]:
    setting, value = line.split("=")
    return setting.strip(), value.strip()


def config_parse(config: list[str]) -> dict[str, Any]:
    try:
        settings: dict[str, str] = dict(map(parse_line, config))
        keys: list[str] = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "SEED",
                           "OUTPUT_FILE", "PERFECT"]
        for key in keys:
            if not settings.get(key):
                raise ValueError(f"Key {key} is missing from configuration "
                                 "file")
        configuration: dict[str, Any] = {}
        configuration["WIDTH"] = int(settings["WIDTH"])
        configuration["HEIGHT"] = int(settings["HEIGHT"])
        configuration["ENTRY"] = tuple(map(lambda x: int(x), settings["ENTRY"].
                                           split(",", maxsplit=2)))
        configuration["EXIT"] = tuple(map(lambda x: int(x), settings["EXIT"].
                                          split(",", maxsplit=2)))
        if settings["SEED"] == "None":
            configuration["SEED"] = eval(settings["SEED"].capitalize())
        else:
            configuration["SEED"] = int(settings["SEED"])
        configuration["OUTPUT_FILE"] = settings["OUTPUT_FILE"]
        configuration["PERFECT"] = eval(settings["PERFECT"].capitalize())
        if configuration["WIDTH"] < 2 or configuration["HEIGHT"] < 2:
            raise ValueError("The maze has a minimum configuration of 2x2")
        if len(configuration["ENTRY"]) > 2:
            raise ValueError("Invalid entry point")
        if len(configuration["EXIT"]) > 2:
            raise ValueError("Invalid exit point")
        if configuration["ENTRY"] == configuration["EXIT"]:
            raise ValueError("Entry and exit set to the same coordenates")
    except ValueError as e:
        print(f"configuration file error: {e}")
        exit(1)
    return configuration
