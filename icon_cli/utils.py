import json
import logging
import os
import typer
from dotenv import load_dotenv
from rich import inspect, print
from rich.logging import RichHandler
from rich.console import Console


def enforce_mainnet(network):
    if network != "mainnet":
        print(
            f"Sorry, this command is only available on mainnet. Your network is currently set to {network}."
        )
        raise typer.Exit()


def format_number_display(input, exa=0, dec=4):
    if isinstance(input, str):
        input = int(input, 16) / 10 ** exa
    if input % 1 == 0:
        dec = 0
    return "{:,.{}f}".format(input, dec)


def hex_to_int(input, exa=None):
    if not exa:
        result = int(input, 16)
    else:
        result = int(input, 16) / 10 ** exa
    return result


def log(message):
    load_dotenv()
    if os.getenv("ENV") == "DEBUG":
        log_level = "DEBUG"
    else:
        log_level = "ERROR"
    logging.basicConfig(
        level=log_level, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
    )
    log = logging.getLogger("rich")
    log.debug(message)


def print_json(input):
    print(json.dumps(input, indent=4))


def print_object(object):
    print("\n")
    inspect(object)
    print("\n")


def print_table(table):
    console = Console()
    print("\n")
    console.print(table)
    print("\n")
