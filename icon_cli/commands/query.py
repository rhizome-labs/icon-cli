import typer
from icon_cli.commands.subcommands.query import balanced, cps, gov
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.models.Icx import Icx
from icon_cli.utils import print_json, print_object
from rich import print

app = typer.Typer()

app.add_typer(balanced.app, name="balanced")
app.add_typer(cps.app, name="cps")
app.add_typer(gov.app, name="gov")


@app.command()
def debug():
    print_object(__name__)


@app.command()
def account(
    address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.validate_network),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    icx = Icx(network)
    account_info = icx.query_address_info(address)

    if format == "json":
        print_json(account_info)
    else:
        print("TBD")


@app.command()
def block(
    block: int = typer.Argument(0, callback=Callbacks.validate_block),
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.validate_network),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    """
    Returns block info for the specified block height.
    """
    icx = Icx(network)
    block_data = icx.query_block(block)

    if format == "json":
        print_json(block_data)
    else:
        print("TBD")


@app.command()
def supply(
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.validate_network),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    icx = Icx(network)
    icx_supply = icx.query_icx_supply()

    if format == "json":
        print_json(icx_supply)


@app.command()
def transaction(
    transaction_hash: str = typer.Argument(...),
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.validate_network),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    icx = Icx(network)
    transaction_result = icx.query_transaction_result(transaction_hash)

    if format == "json":
        print_json(transaction_result)
    else:
        print("TBD")
