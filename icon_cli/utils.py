import json
import os
from pathlib import Path

import typer
from rich import print


class Utils:
    def __init__(self) -> None:
        pass

    @classmethod
    def abs_path(cls, relative_path: str) -> Path:
        """
        A function that converts a relative path to an absolute path.
        """
        return os.path.abspath(relative_path)

    @classmethod
    def exit(cls, message: str, level: str = None):
        """
        A function that formats and prints an error message before exiting the program.
        """
        # Set color and prefix for die message.
        if level == "error":
            fg = "red"
            prefix = "ERROR: "
        elif level == "warning":
            fg = "orange"
            prefix = "WARNING: "
        elif level == "ok":
            fg = "green"
            prefix = "OK: "
        elif level == "success":
            fg = "green"
            prefix = "SUCCESS: "
        else:
            fg = None
            prefix = None

        # Print die message.
        typer.secho(f"{prefix}{message}", fg=fg)

        # Exit application.
        raise typer.Exit()

    @classmethod
    def print_json(cls, input: dict, sort_keys: bool = False) -> str:
        if sort_keys is True:
            print(json.dumps(input, indent=4, sort_keys=True))
        else:
            print(json.dumps(input, indent=4))

    @classmethod
    def strip_all_whitespace(cls, input: str, force_lowercase: bool):
        """
        A function that strips all whitespace from a string.
        """
        input = input.strip()
        input = input.replace(" ", "")
        # Convert to lowercase if force_lowercase is True.
        if force_lowercase is True:
            input = input.casefold()
        return input
