import typer
from icon_cli.commands.subcommands.config import address_book, wallet
from icon_cli.config import Config
from icon_cli.validators import Validators
from rich import inspect, print

app = typer.Typer()

app.add_typer(address_book.app, name="address-book")
app.add_typer(wallet.app, name="wallet")


@app.command()
def debug():
    inspect(__name__)


@app.command()
def inspect():
    config = Config.inspect_config()
    print(config)


@app.command()
def set_network(
    network: str = typer.Argument(..., callback=Validators.validate_network)
):
    """
    Sets the value for "default_network" in config.yml.
    """
    Config.set_default_network(network)
