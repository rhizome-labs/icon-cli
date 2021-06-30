import json
from rich import print
from rich.console import Console


def print_json(input):
    print(json.dumps(input, indent=4))


def print_table(table):
    console = Console()
    console.print(table)
