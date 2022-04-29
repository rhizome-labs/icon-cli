import logging
import os

import typer
from dotenv import load_dotenv
from rich import inspect
from rich.logging import RichHandler

load_dotenv()


def die(message: str, level: str = None):
    if level == "error":
        fg = "red"
        prefix = "ERROR: "
    elif level == "warning":
        fg = "orange"
        prefix = "WARNING: "
    else:
        fg = None
        prefix = None
    typer.secho(f"{prefix}{message}", fg=fg)
    raise typer.Exit()


def format(value: int, exa: int, round: int = 0):
    if round == 0:
        return f"{value / 10**exa}"
    else:
        return f"{round(value / 10**exa, round)}"


def hex_to_int(input: str):
    return int(input, 16)


def log(message):

    if os.getenv("ENV") == "DEBUG":
        log_level = "DEBUG"
    else:
        log_level = "INFO"

    logging.basicConfig(
        level=log_level, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
    )

    log = logging.getLogger("rich")

    if log_level == "DEBUG":
        inspect(message)
        log.debug(message)
