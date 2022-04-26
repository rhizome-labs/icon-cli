import typer
from icon_cli.commands.subcommands.config import address_book
from icon_cli.config import Config
from icon_cli.validators import Validators
from rich import inspect, print

app = typer.Typer()

app.add_typer(address_book.app, name="address-book")


@app.command()
def debug():
    inspect(__name__)


@app.command()
def inspect():
    config = Config.inspect_config()
    print(config)
