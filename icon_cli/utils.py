import json
import logging
import os
import typer
from decimal import Decimal
from dotenv import load_dotenv
from rich import box, inspect, print
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table


def kv_table(rows: list, title="None"):
    table = Table(
            box=box.DOUBLE,
            show_lines=True,
            show_header=False,
            title=title,
            title_justify="left",
            title_style="bold",
        )

    table.add_column("Key", justify="left")
    table.add_column("Value", justify="left")

    for row in rows:
        table.add_row(row[0], row[1])

    print_table(table)


def enforce_mainnet(network):
    if network != "mainnet":
        print(
            f"Sorry, this command is only available on mainnet. Your network is currently set to {network}."
        )
        raise typer.Exit()


def die(message: str = "Exiting now..."):
    print(message)
    raise typer.Exit()


def format_number_display(input, exa=0, dec=4):
    if isinstance(input, str) and input[:2] == "0x":
        input = Decimal(int(input, 16) / 10 ** exa)
    elif isinstance(input, int) or isinstance(input, float):
        input = Decimal(input) / 10 ** exa
    if input % 1 == 0:
        output = "{:,.{}f}".format(input, 0)
    else:
        output = "{:,.{}f}".format(input, dec).rstrip("0")
    return output


def from_loop(value):
    icx = value / 10 ** 18
    return icx


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
        log_level = "INFO"

    logging.basicConfig(
        level=log_level, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
    )
    
    log = logging.getLogger("rich")

    if log_level == "DEBUG":
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


def print_tx_hash(transaction_result: dict):
    print(f"Transaction Hash: {transaction_result['txHash']}")


def to_loop(value):
    loop = int(value * 10 ** 18)
    return loop
